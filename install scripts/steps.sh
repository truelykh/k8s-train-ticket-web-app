# Kubernetes HA Cluster Setup on RHEL 9 EC2

## 1. Architecture

The final environment consists of 8 EC2 instances:

| Role                          | Hostname     | Private IP |
| ----------------------------- | ------------ | ---------: |
| Bastion + Nginx Load Balancer | bastion      | 10.0.0.247 |
| Control Plane 1               | kube-cp1     | 10.0.0.117 |
| Control Plane 2               | kube-cp2     |  10.0.0.19 |
| Worker 1                      | kube-wnode-1 | 10.0.0.130 |
| Worker 2                      | kube-wnode-2 | 10.0.0.193 |
| Worker 3                      | kube-wnode-3 |  10.0.0.27 |
| Worker 4                      | kube-wnode-4 |  10.0.0.16 |
| Worker 5                      | kube-wnode-5 | 10.0.0.161 |

Kubernetes version:

```text
v1.32.13
```

Container runtime:

```text
containerd
```

CNI:

```text
Calico
```

Pod CIDR:

```text
192.168.0.0/16
```

Kubernetes API endpoint:

```text
10.0.0.247:6443
```

Traffic flow:

```text
                    Client
                      |
                      v
             +----------------+
             | Bastion + Nginx|
             | 10.0.0.247     |
             | TCP :6443      |
             +-------+--------+
                     |
             Nginx TCP LB
                /         \
               /           \
              v             v
       +-------------+ +-------------+
       |   kube-cp1  | |   kube-cp2  |
       | 10.0.0.117  | |  10.0.0.19  |
       | Control      | | Control      |
       | Plane        | | Plane        |
       +------+------+ +------+-------+
              \               /
               \             /
                +-----------+
                      |
                Kubernetes
                   Cluster
                      |
        +------+------+------+------+------+
        |      |      |      |      |
        v      v      v      v      v
       W1     W2     W3     W4     W5
```

---

# 2. Kubernetes Node Preparation

The same Kubernetes prerequisites were applied to the control-plane and worker nodes.

## Disable swap

```bash
sudo swapoff -a
```

Verify:

```bash
swapon --show
```

No output should be returned.

## Configure SELinux

For the cluster setup:

```bash
sudo setenforce 0
```

Verify:

```bash
getenforce
```

Expected:

```text
Permissive
```

## Load kernel modules

```bash
sudo modprobe overlay
sudo modprobe br_netfilter
```

Persist them:

```bash
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF
```

## Configure Kubernetes networking

```bash
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward = 1
EOF
```

Apply:

```bash
sudo sysctl --system
```

Verify:

```bash
sysctl net.ipv4.ip_forward
```

Expected:

```text
net.ipv4.ip_forward = 1
```

---

# 3. Install containerd

Install containerd:

```bash
sudo dnf install -y containerd
```

Generate configuration:

```bash
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml
```

Enable systemd cgroups.

Edit:

```bash
sudo vi /etc/containerd/config.toml
```

Set:

```toml
SystemdCgroup = true
```

Restart:

```bash
sudo systemctl restart containerd
sudo systemctl enable containerd
```

Verify:

```bash
systemctl status containerd
```

---

# 4. Install Kubernetes v1.32 Packages

Create the Kubernetes repository:

```bash
cat <<'EOF' | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.32/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.32/rpm/repodata/repomd.xml.key
exclude=kubelet kubeadm kubectl cri-tools kubernetes-cni
EOF
```

Install:

```bash
sudo dnf install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
```

Enable kubelet:

```bash
sudo systemctl enable kubelet
```

Verify:

```bash
kubeadm version
kubectl version --client
```

Target version:

```text
v1.32.13
```

---

# 5. Configure Nginx on Bastion

The Bastion acts as the Kubernetes API TCP load balancer.

Install:

```bash
sudo dnf install -y nginx nginx-mod-stream nmap-ncat
```

The Nginx stream module was available at:

```text
/usr/lib64/nginx/modules/ngx_stream_module.so
```

The module configuration is loaded through:

```nginx
include /usr/share/nginx/modules/*.conf;
```

## Nginx configuration

The final configuration is:

```nginx
upstream kube {
    server 10.0.0.117:6443;
    server 10.0.0.19:6443;
}

server {
    listen 6443;
    proxy_pass kube;
}
```

File:

```text
/etc/nginx/conf.d/kube.conf
```

The top-level Nginx configuration contains:

```nginx
stream {
    include /etc/nginx/conf.d/*.conf;
}
```

Test:

```bash
sudo nginx -t
```

Reload:

```bash
sudo systemctl reload nginx
```

---

# 6. RHEL SELinux Configuration for Nginx

SELinux initially prevented Nginx from binding to TCP 6443.

Add port 6443 to the HTTP port type:

```bash
sudo semanage port -a -t http_port_t -p tcp 6443
```

Verify:

```bash
sudo semanage port -l | grep http_port_t
```

Nginx also needed permission to connect to the Kubernetes API servers.

Enable:

```bash
sudo setsebool -P httpd_can_network_connect 1
```

Verify:

```bash
getsebool httpd_can_network_connect
```

Expected:

```text
httpd_can_network_connect --> on
```

---

# 7. Verify Nginx Before Kubernetes Initialization

Test the API endpoint:

```bash
curl -k https://10.0.0.247:6443/version
```

and:

```bash
curl -k https://10.0.0.247:6443/readyz
```

Expected:

```text
ok
```

The `-k` option is used because the Kubernetes API certificate is not trusted by the normal system CA store.

---

# 8. Initialize Control Plane 1

On:

```text
kube-cp1
10.0.0.117
```

Run:

```bash
sudo kubeadm init \
  --control-plane-endpoint=10.0.0.247:6443 \
  --pod-network-cidr=192.168.0.0/16 \
  --upload-certs
```

The important point is:

```text
--control-plane-endpoint=10.0.0.247:6443
```

The Kubernetes API is therefore exposed through the Nginx load balancer rather than directly through CP1.

---

# 9. Configure kubectl on CP1

After initialization:

```bash
mkdir -p $HOME/.kube

sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config

sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

Verify:

```bash
kubectl get nodes
```

Initially CP1 was:

```text
kube-cp1   NotReady   control-plane
```

This was expected because the CNI had not yet been installed.

The Kubernetes control-plane containers were running:

```text
etcd
kube-apiserver
kube-controller-manager
kube-scheduler
kube-proxy
```

---

# 10. Install Calico

Calico was installed on CP1:

```bash
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.31.0/manifests/calico.yaml
```

Calico uses:

```text
192.168.0.0/16
```

which matches the Pod CIDR used during `kubeadm init`.

Verify:

```bash
kubectl get pods -A
```

and:

```bash
kubectl get nodes
```

CP1 should become:

```text
kube-cp1   Ready   control-plane
```

---

# 11. Generate Control Plane Join Information

On CP1:

```bash
sudo kubeadm token create --print-join-command
```

Example:

```bash
kubeadm join 10.0.0.247:6443 \
  --token <TOKEN> \
  --discovery-token-ca-cert-hash sha256:<HASH>
```

Generate the control-plane certificate key:

```bash
sudo kubeadm init phase upload-certs --upload-certs
```

The generated certificate key is required when joining another control-plane node.

---

# 12. Join Control Plane 2

CP2:

```text
kube-cp2
10.0.0.19
```

The CP2 join command has these additional parameters:

```text
--control-plane
--certificate-key <CERTIFICATE-KEY>
```

Example:

```bash
sudo kubeadm join 10.0.0.247:6443 \
  --token <TOKEN> \
  --discovery-token-ca-cert-hash sha256:<HASH> \
  --control-plane \
  --certificate-key <CERTIFICATE-KEY>
```

After joining, verify on CP2:

```bash
sudo crictl ps
```

Expected control-plane containers:

```text
etcd
kube-apiserver
kube-controller-manager
kube-scheduler
kube-proxy
calico-node
```

## Configure kubectl on CP2

```bash
mkdir -p $HOME/.kube

sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config

sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

Then:

```bash
kubectl get nodes
```

---

# 13. Calico on CP2

Calico does not need to be manually installed again.

Calico runs as a DaemonSet, so when CP2 joins the cluster, a `calico-node` pod is automatically created for CP2.

Verify:

```bash
kubectl get pods -n kube-system -o wide | grep calico
```

There should be a Calico node pod on CP2.

---

# 14. Add CP2 to Nginx

After confirming CP2's API server works:

```bash
curl -k https://10.0.0.19:6443/readyz
```

Expected:

```text
ok
```

Update Nginx:

```nginx
upstream kube {
    server 10.0.0.117:6443;
    server 10.0.0.19:6443;
}

server {
    listen 6443;
    proxy_pass kube;
}
```

Test:

```bash
sudo nginx -t
```

Reload:

```bash
sudo systemctl reload nginx
```

Test HA endpoint:

```bash
curl -k https://10.0.0.247:6443/readyz
```

Expected:

```text
ok
```

---

# 15. Join Worker Nodes

Worker nodes:

```text
10.0.0.130
10.0.0.193
10.0.0.27
10.0.0.16
10.0.0.161
```

Generate the worker join command from CP1:

```bash
sudo kubeadm token create --print-join-command
```

Example:

```bash
sudo kubeadm join 10.0.0.247:6443 \
  --token <TOKEN> \
  --discovery-token-ca-cert-hash sha256:<HASH>
```

Run this command on each worker.

### Important

Workers do NOT use:

```text
--control-plane
--certificate-key
```

Those parameters are only for additional control-plane nodes.

---

# 16. Calico on Workers

Calico is automatically deployed to each worker because it is a DaemonSet.

Do not manually install Calico separately on every worker.

Verify:

```bash
kubectl get pods -n kube-system -o wide | grep calico-node
```

There should eventually be one `calico-node` pod per Kubernetes node.

---

# 17. Final Cluster Verification

Run from CP1 or CP2:

```bash
kubectl get nodes -o wide
```

Final result:

```text
NAME           STATUS   ROLES           VERSION
kube-cp1       Ready    control-plane   v1.32.13
kube-cp2       Ready    control-plane   v1.32.13
kube-wnode-1   Ready    <none>          v1.32.13
kube-wnode-2   Ready    <none>          v1.32.13
kube-wnode-3   Ready    <none>          v1.32.13
kube-wnode-4   Ready    <none>          v1.32.13
kube-wnode-5   Ready    <none>          v1.32.13
```

Verify Calico:

```bash
kubectl get pods -n kube-system -o wide | grep calico-node
```

Verify all cluster pods:

```bash
kubectl get pods -A
```

Verify the HA API endpoint:

```bash
curl -k https://10.0.0.247:6443/readyz
```

Expected:

```text
ok
```

---

# 18. Configure kubectl on Bastion

The Bastion is:

```text
10.0.0.247
```

The desired management flow is:

```text
kubectl
   |
   v
10.0.0.247:6443
   |
   v
Nginx TCP Load Balancer
   |
   +----> CP1 :6443
   |
   +----> CP2 :6443
```

## Install kubectl on Bastion

Use the Kubernetes v1.32 repository:

```bash
cat <<'EOF' | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.32/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.32/rpm/repodata/repomd.xml.key
exclude=kubelet kubeadm kubectl cri-tools kubernetes-cni
EOF
```

Install:

```bash
sudo dnf install -y kubectl --disableexcludes=kubernetes
```

Verify:

```bash
kubectl version --client
```

---

# 19. SSH Agent Forwarding for Bastion → CP1

The private key:

```text
kube-ssh.pem
```

remains on the Mac.

On the Mac:

```bash
chmod 400 kube-ssh.pem
```

Add it to the SSH agent:

```bash
ssh-add ./kube-ssh.pem
```

Verify:

```bash
ssh-add -l
```

Connect to Bastion with agent forwarding:

```bash
ssh -A -i kube-ssh.pem ec2-user@<BASTION_PUBLIC_IP>
```

Verify on Bastion:

```bash
echo "$SSH_AUTH_SOCK"
```

It should return a path such as:

```text
/tmp/ssh-XXXX/agent.xxxxx
```

Verify the forwarded key:

```bash
ssh-add -l
```

Then test Bastion → CP1:

```bash
ssh ec2-user@10.0.0.117
```

If this succeeds, the Bastion can authenticate to CP1 without storing the `.pem` file on Bastion.

---

# 20. Copy admin.conf to Bastion

On CP1, create a temporary readable copy:

```bash
sudo cp /etc/kubernetes/admin.conf /tmp/admin.conf
sudo chmod 644 /tmp/admin.conf
```

Exit CP1.

On Bastion:

```bash
mkdir -p ~/.kube

scp ec2-user@10.0.0.117:/tmp/admin.conf ~/.kube/config
```

Secure it:

```bash
chmod 600 ~/.kube/config
```

---

# 21. Point Bastion kubectl to Nginx

Check:

```bash
grep server ~/.kube/config
```

If it contains:

```text
server: https://10.0.0.117:6443
```

change it to the HA endpoint:

```bash
sed -i 's#https://10.0.0.117:6443#https://10.0.0.247:6443#' ~/.kube/config
```

Verify:

```bash
grep server ~/.kube/config
```

Expected:

```text
server: https://10.0.0.247:6443
```

Now:

```bash
kubectl get nodes
```

The command is now going through:

```text
Bastion kubectl
       |
       v
10.0.0.247:6443
       |
       v
Nginx
   /       \
  v         v
CP1       CP2
```

---

# 22. Remove Temporary admin.conf

After confirming the Bastion kubeconfig works:

```bash
ssh ec2-user@10.0.0.117 'sudo rm -f /tmp/admin.conf'
```

The private key remains on the Mac.

---

# 23. Final Operational Model

The completed environment is:

```text
                         ADMIN
                           |
                           v
                    +-------------+
                    |   BASTION   |
                    | 10.0.0.247  |
                    |    NGINX    |
                    +------+------+
                           |
                     TCP :6443
                           |
                +----------+----------+
                |                     |
                v                     v
        +---------------+     +---------------+
        |    CP1        |     |    CP2        |
        | 10.0.0.117    |     | 10.0.0.19     |
        | Control Plane  |     | Control Plane |
        +-------+-------+     +-------+-------+
                \                     /
                 \                   /
                  +-------+---------+
                          |
                    Kubernetes API
                          |
        +---------+-------+-------+---------+
        |         |       |       |         |
        v         v       v       v         v
       W1        W2      W3      W4        W5
     .130      .193    .27     .16       .161

                    CALICO CNI
                 Pod CIDR:
              192.168.0.0/16
```

## Final Status

```text
Infrastructure       : 8 EC2 instances
Kubernetes nodes     : 7
Control planes       : 2
Workers              : 5
API Load Balancer    : Nginx
LB endpoint          : 10.0.0.247:6443
CNI                  : Calico
Pod CIDR             : 192.168.0.0/16
Kubernetes version   : v1.32.13
Container runtime    : containerd
All nodes            : Ready
HA API endpoint      : Working
Bastion kubectl      : Configured
```

The Bastion is therefore both the **SSH jump host** and the **Kubernetes API load-balancing endpoint**, while CP1 and CP2 provide the redundant Kubernetes control plane.

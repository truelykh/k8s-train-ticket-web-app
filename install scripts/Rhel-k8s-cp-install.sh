#!/bin/bash
# RHEL 8/9 Kubernetes Control Plane Installation Script

echo "Starting Kubernetes Control Plane Installation..."

# 1. Disable Swap
echo "Disabling swap..."
sudo swapoff -a
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab

# 2. Set SELinux to permissive
echo "Setting SELinux to permissive..."
sudo setenforce 0
sudo sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

# 3. Configure firewall and network modules
echo "Loading kernel modules..."
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF
sudo modprobe overlay
sudo modprobe br_netfilter

echo "Configuring sysctl params for Kubernetes..."
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF
sudo sysctl --system

# 4. Install Containerd
echo "Installing containerd..."
sudo dnf install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo dnf install -y containerd.io
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml >/dev/null
# Set SystemdCgroup = true
sudo sed -i 's/SystemdCgroup \= false/SystemdCgroup \= true/g' /etc/containerd/config.toml
sudo systemctl restart containerd
sudo systemctl enable containerd

# 5. Add Kubernetes Repository (using 1.28 as example, adjust if needed)
echo "Adding Kubernetes repository..."
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.28/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.28/rpm/repodata/repomd.xml.key
exclude=kubelet kubeadm kubectl cri-tools kubernetes-cni
EOF

# 6. Install Kubernetes Components
echo "Installing kubelet, kubeadm, and kubectl..."
sudo dnf install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
sudo systemctl enable --now kubelet

# 7. Initialize Control Plane
echo "Initializing Kubernetes Control Plane..."
sudo kubeadm init --pod-network-cidr=192.168.0.0/16

# 8. Setup Kubeconfig for root user
echo "Setting up kubeconfig..."
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# 9. Install Calico CNI
echo "Installing Calico Network Plugin..."
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/tigera-operator.yaml
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/custom-resources.yaml

kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.31.0/manifests/calico.yaml

echo "========================================="
echo "Control Plane installation complete!"
echo "Please save the 'kubeadm join' command printed above to use on your worker nodes."
echo "Wait a few minutes for pods to be ready (kubectl get pods -A)"
echo "========================================="


kubeadm join 10.0.0.28:6443 --token ratz7g.kmxsnsofimpo0p0v \
	--discovery-token-ca-cert-hash sha256:7ae0501a59cfe784b87e9ed6a973e7d988c959c34325e85043f3251e81a02fad 


kubeadm init \
  --control-plane-endpoint=10.0.0.69:6443 \
  --pod-network-cidr=192.168.0.0/16 \
  --upload-certs \
  --ignore-preflight-errors=Mem


  ```bash
#!/bin/bash

echo "Starting Kubernetes 1.32 Control Plane Installation..."

sudo swapoff -a
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab

sudo setenforce 0
sudo sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

sudo sysctl --system

sudo dnf install -y yum-utils

sudo yum-config-manager \
  --add-repo https://download.docker.com/linux/centos/docker-ce.repo

sudo dnf install -y containerd.io

sudo mkdir -p /etc/containerd

containerd config default | sudo tee /etc/containerd/config.toml >/dev/null

sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/g' \
  /etc/containerd/config.toml

sudo systemctl restart containerd
sudo systemctl enable containerd

cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.32/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.32/rpm/repodata/repomd.xml.key
exclude=kubelet kubeadm kubectl cri-tools kubernetes-cni
EOF

sudo dnf clean all
sudo dnf makecache

sudo dnf install -y kubelet kubeadm kubectl \
  --disableexcludes=kubernetes

sudo systemctl enable --now kubelet

echo ""
echo "Kubernetes Installation Complete"
echo ""
kubeadm version
kubectl version --client
kubelet --version
containerd --version
```

Bastion: 10.0.0.247
CP1: 10.0.0.117
CP2: 10.0.0.19
Worker1: 10.0.0.130 
Worker2: 10.0.0.193
Worker3: 10.0.0.27
Worker4: 10.0.0.16
Worker5: 10.0.0.161


kubeadm join 10.0.0.247:6443 --token xhb7fv.g800a63vwjgsfav3 \
	--discovery-token-ca-cert-hash sha256:22d89f9d795c5bf9a6999ebb98d68926f6ac6a5a5c8e21af9c31128ff1fcd7bf

---

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

Alternatively, if you are the root user, you can run:

  export KUBECONFIG=/etc/kubernetes/admin.conf

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

You can now join any number of control-plane nodes running the following command on each as root:

  kubeadm join 10.0.0.247:6443 --token xhb7fv.g800a63vwjgsfav3 \
	--discovery-token-ca-cert-hash sha256:22d89f9d795c5bf9a6999ebb98d68926f6ac6a5a5c8e21af9c31128ff1fcd7bf \
	--control-plane --certificate-key 5cc644f8356ce7c8915daab43200426d3e73b96e56beee834c577149ad81647e

Please note that the certificate-key gives access to cluster sensitive data, keep it secret!
As a safeguard, uploaded-certs will be deleted in two hours; If necessary, you can use
"kubeadm init phase upload-certs --upload-certs" to reload certs afterward.

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 10.0.0.247:6443 --token xhb7fv.g800a63vwjgsfav3 \
	--discovery-token-ca-cert-hash sha256:22d89f9d795c5bf9a6999ebb98d68926f6ac6a5a5c8e21af9c31128ff1fcd7bf 

---



sudo kubeadm join 10.0.0.247:6443 \
  --token zfrskb.2jpl2eal83x5r4x1 \
  --discovery-token-ca-cert-hash sha256:22d89f9d795c5bf9a6999ebb98d68926f6ac6a5a5c8e21af9c31128ff1fcd7bf
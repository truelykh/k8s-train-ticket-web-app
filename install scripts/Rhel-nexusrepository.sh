#!/bin/bash
# RHEL 8/9 Nexus Repository Manager Installation Script

echo "Starting Nexus Repository Installation..."

# 1. Install Java 8 (Required for Nexus 3)
echo "Installing OpenJDK 8..."
sudo dnf install -y java-1.8.0-openjdk wget

# 2. Download and extract Nexus
echo "Downloading Nexus..."
cd /opt
sudo wget -O nexus.tar.gz https://download.sonatype.com/nexus/3/latest-unix.tar.gz
sudo tar -zxvf nexus.tar.gz
sudo rm -f nexus.tar.gz
# Rename directory to 'nexus' for easier management
sudo mv nexus-* nexus

# 3. Create Nexus User for Security
echo "Creating nexus user..."
sudo useradd nexus
sudo chown -R nexus:nexus /opt/nexus
sudo chown -R nexus:nexus /opt/sonatype-work

# 4. Configure Nexus to run as 'nexus' user
echo "Configuring nexus user..."
sudo sed -i 's/#run_as_user=""/run_as_user="nexus"/' /opt/nexus/bin/nexus.rc

# 5. Create Systemd Service File
echo "Creating systemd service..."
cat <<EOF | sudo tee /etc/systemd/system/nexus.service
[Unit]
Description=Nexus Service
After=network.target

[Service]
Type=forking
LimitNOFILE=65536
User=nexus
Group=nexus
ExecStart=/opt/nexus/bin/nexus start
ExecStop=/opt/nexus/bin/nexus stop
User=nexus
Restart=on-abort
TimeoutSec=600

[Install]
WantedBy=multi-user.target
EOF

# 6. Start and Enable Nexus
echo "Starting Nexus service..."
sudo systemctl daemon-reload
sudo systemctl enable nexus
sudo systemctl start nexus

# 7. Configure Firewall
echo "Opening firewall port 8081..."
sudo firewall-cmd --permanent --zone=public --add-port=8081/tcp
sudo firewall-cmd --reload

echo "========================================="
echo "Nexus installation complete!"
echo "It may take a few minutes for Nexus to start completely."
echo "You can access Nexus at http://<your_server_ip>:8081"
echo "Initial Admin Password:"
sudo cat /opt/sonatype-work/nexus3/admin.password
echo "========================================="

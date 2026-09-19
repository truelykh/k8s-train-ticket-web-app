#!/bin/bash
# RHEL 8/9 Nginx Installation Script

echo "Starting Nginx Installation..."

# 1. Install EPEL Repository
echo "Installing EPEL repository..."
sudo dnf install -y epel-release

# 2. Install Nginx
echo "Installing Nginx..."
sudo dnf install -y nginx

# 3. Start and Enable Nginx
echo "Starting Nginx service..."
sudo systemctl enable nginx
sudo systemctl start nginx

# 4. Configure Firewall
echo "Opening firewall ports 80 and 443..."
sudo firewall-cmd --permanent --zone=public --add-service=http
sudo firewall-cmd --permanent --zone=public --add-service=https
sudo firewall-cmd --reload

echo "========================================="
echo "Nginx installation complete!"
echo "You can view the default Nginx page at http://<your_server_ip>"
echo "========================================="

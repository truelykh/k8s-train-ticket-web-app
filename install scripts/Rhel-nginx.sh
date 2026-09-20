#!/bin/bash
# RHEL 8/9 Nginx Installation Script

set -e

echo "Starting Nginx Installation..."

echo "Installing Nginx..."
sudo dnf install -y nginx

echo "Starting and enabling Nginx service..."
sudo systemctl enable --now nginx

echo "Opening firewall ports 80 and 443..."
sudo firewall-cmd --permanent --zone=public --add-service=http
sudo firewall-cmd --permanent --zone=public --add-service=https
sudo firewall-cmd --reload

echo "========================================="
echo "Nginx installation complete!"
echo "You can view the default Nginx page at http://$(curl -s ifconfig.me || echo '<your_server_ip>')"
echo "========================================="
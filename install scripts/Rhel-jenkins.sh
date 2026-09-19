#!/bin/bash
# RHEL 8/9 Jenkins Installation Script

echo "Starting Jenkins Installation..."

# 1. Install prerequisites (Java 17 is recommended for modern Jenkins)
echo "Installing OpenJDK 17..."
sudo dnf install -y fontconfig java-17-openjdk

# 2. Add the Jenkins repository
echo "Adding Jenkins repository..."
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key

# 3. Install Jenkins
echo "Installing Jenkins..."
sudo dnf install -y jenkins

# 4. Enable and start Jenkins service
echo "Starting Jenkins service..."
sudo systemctl daemon-reload
sudo systemctl enable jenkins
sudo systemctl start jenkins

# 5. Configure Firewall
echo "Opening firewall port 8080..."
sudo firewall-cmd --permanent --zone=public --add-port=8080/tcp
sudo firewall-cmd --reload

echo "========================================="
echo "Jenkins installation complete!"
echo "You can access Jenkins at http://<your_server_ip>:8080"
echo "Initial Admin Password:"
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
echo "========================================="

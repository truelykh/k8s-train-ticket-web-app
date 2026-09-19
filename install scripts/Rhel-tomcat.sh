#!/bin/bash
# RHEL 8/9 Apache Tomcat Installation Script

echo "Starting Apache Tomcat Installation..."

# 1. Install Java 11 (Tomcat 9 runs well on Java 11)
echo "Installing OpenJDK 11..."
sudo dnf install -y java-11-openjdk wget tar

# 2. Create Tomcat User
echo "Creating tomcat user..."
sudo useradd -m -U -d /opt/tomcat -s /bin/false tomcat

# 3. Download and Extract Tomcat
echo "Downloading Tomcat 9..."
cd /tmp
wget https://downloads.apache.org/tomcat/tomcat-9/v9.0.87/bin/apache-tomcat-9.0.87.tar.gz
sudo tar -xf apache-tomcat-9.0.87.tar.gz -C /opt/tomcat/
sudo mv /opt/tomcat/apache-tomcat-9.0.87/* /opt/tomcat/
sudo rm -rf /opt/tomcat/apache-tomcat-9.0.87

# 4. Set Permissions
echo "Setting permissions..."
sudo chown -R tomcat: /opt/tomcat
sudo sh -c 'chmod +x /opt/tomcat/bin/*.sh'

# 5. Create Systemd Service File
echo "Creating systemd service..."
cat <<EOF | sudo tee /etc/systemd/system/tomcat.service
[Unit]
Description=Tomcat 9 servlet container
After=network.target

[Service]
Type=forking
User=tomcat
Group=tomcat
Environment="JAVA_HOME=/usr/lib/jvm/jre"
Environment="JAVA_OPTS=-Djava.security.egd=file:///dev/urandom"
Environment="CATALINA_BASE=/opt/tomcat"
Environment="CATALINA_HOME=/opt/tomcat"
Environment="CATALINA_PID=/opt/tomcat/temp/tomcat.pid"
Environment="CATALINA_OPTS=-Xms512M -Xmx1024M -server -XX:+UseParallelGC"
ExecStart=/opt/tomcat/bin/startup.sh
ExecStop=/opt/tomcat/bin/shutdown.sh

[Install]
WantedBy=multi-user.target
EOF

# 6. Start and Enable Tomcat
echo "Starting Tomcat service..."
sudo systemctl daemon-reload
sudo systemctl enable tomcat
sudo systemctl start tomcat

# 7. Configure Firewall
echo "Opening firewall port 8080..."
sudo firewall-cmd --permanent --zone=public --add-port=8080/tcp
sudo firewall-cmd --reload

echo "========================================="
echo "Tomcat installation complete!"
echo "You can access Tomcat at http://<your_server_ip>:8080"
echo "========================================="

#!/bin/bash
# ============================================================
# ec2-setup.sh — Bootstrap script for AWS EC2 Ubuntu instance
# Virtualization Using Cloud Computing Project
# VIT Chennai, 2026
# ============================================================

set -e

echo "============================================"
echo " EC2 Bootstrap: Virtualization Project Setup"
echo "============================================"

# Update packages
echo "[1/6] Updating system packages..."
sudo apt update -y && sudo apt upgrade -y

# Install Python and pip
echo "[2/6] Installing Python 3 and pip..."
sudo apt install -y python3 python3-pip git curl

# Install Docker
echo "[3/6] Installing Docker..."
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker

# Add current user to docker group (no sudo needed after re-login)
sudo usermod -aG docker $USER
echo "      Note: Log out and back in for docker group to take effect."

# Clone the repository
echo "[4/6] Cloning project repository..."
cd ~
git clone https://github.com/tanisha-ahl/virtualization-using-cloud-computing.git
cd virtualization-using-cloud-computing

# Install Python dependencies
echo "[5/6] Installing Python dependencies..."
pip3 install -r requirements.txt

# Start Docker containers
echo "[6/6] Launching Docker containers..."
sudo docker run -d -p 8081:80 --name nginx-container nginx
sudo docker run -d -p 8082:80 --name httpd-container httpd

echo ""
echo "============================================"
echo " Setup Complete!"
echo "============================================"
echo " Running containers:"
sudo docker ps

echo ""
echo " Verify containers:"
echo "   curl http://localhost:8081   -> Nginx"
echo "   curl http://localhost:8082   -> HTTPD"
echo ""
echo " Start Flask API:"
echo "   python3 app.py"
echo ""
echo " API will be accessible at:"
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo "<your-ec2-public-ip>")
echo "   http://$PUBLIC_IP:5000"
echo "   http://$PUBLIC_IP:5000/info"
echo "   http://$PUBLIC_IP:5000/containers"
echo "============================================"

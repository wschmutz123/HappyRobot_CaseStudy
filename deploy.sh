#!/bin/bash
# Install system dependencies
sudo amazon-linux-extras enable epel
sudo yum install -y python3 python3-pip npm

cd ~/HappyRobot_CaseStudy/Backend

# Setup Python virtual environment
if [ ! -d "env" ]; then
    python3 -m venv env
fi
source env/bin/activate
pip install -r requirements.txt

# Make sure start.sh is executable
chmod +x start.sh

# Start app with PM2 using your start.sh
pm2 start start.sh --name happyrobot-app

# Ensure PM2 restarts on reboot
pm2 startup systemd
pm2 save

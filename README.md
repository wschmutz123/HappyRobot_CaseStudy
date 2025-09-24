# HappyRobot_CaseStudy

## FastAPI Deployment on AWS EC2 with docker-compose, Nginx, and Let’s Encrypt

## To access HappyRobot Deployment:

  - Go to `https://willhappyrobot.ddns.net`

## To Reproduce Deployment:

Prerequisites:
  - EC2 instance running Amazon Linux 2 or 2023
  - SSH access to the instance
  - Domain pointing to your EC2 (e.g., willhappyrobot.ddns.net)
  - Security group rules:
      - Allow 80 (HTTP), Allow 443 (HTTPS), Allow 22 (SSH)

### Steps:

1. SSH into the instance, Install git, and Clone the Repo:
   `ssh -i <YOUR_KEY.pem> ec2-user@<EC2_PUBLIC_IP>`

    ```bash
    # Update system
    sudo yum update -y
    sudo yum install -y git
    cd ~
    git clone https://github.com/wschmutz123/HappyRobot_CaseStudy.git
    ```
2. Install Docker & docker-compose (v1):
   
   ```bash
    
    # Install Docker
    sudo yum install -y docker
    sudo systemctl enable --now docker
    
    # Add ec2-user to docker group
    sudo usermod -aG docker ec2-user
    exec bash
    
    # Install docker-compose v1 (standalone)
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" \
      -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    
    # Verify installation
    docker --version
    docker-compose --version
   ```
   
6. Create .env file with REST API key and WEB TOKEN for your FMCSA api:
   
   ```bash
   cd ~/HappyRobot_CaseStudy/Backend
   touch .env
   echo "REST_API_KEY=<YOUR_SECRET_KEY>" > .env
   echo "WEB_TOKEN=<YOUR_WEB_TOKEN>" > .env

7. Make deploy.sh executable and run the deployment Script:
   ```bash
    chmod +x deploy.sh
    ./deploy.sh
  
  This will:
  
  - Install system dependencies (Python 3, pip, npm, Certbot)
  - Set up Python virtual environment and install dependencies
  - Make start.sh executable and start the FastAPI app with PM2
  - Configure PM2 to auto-start on server reboot

5. Access the API:
   
  URL: https://willhappyrobot.ddns.net:3001 (or your specific domain name)

  API Key Header: X-API-Key: <YOUR_SECRET_KEY>

  Example:

  ```bash
  curl -H "X-API-Key: <YOUR_SECRET_KEY>" \
  "https://willhappyrobot.ddns.net:3001/api/search_loads?origin=Dallas"
  ```

Notes:
  - Ensure ports 3001 (API) and 80 (HTTP for Let's Encrypt) are open in your EC2 security group.
  - Recommended to use a domain with Let’s Encrypt for HTTPS; self-signed certificates are suitable for testing only.
  - The deployment script is idempotent, so running it multiple times won’t break your app.


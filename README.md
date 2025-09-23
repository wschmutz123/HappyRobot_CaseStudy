# HappyRobot_CaseStudy

## FastAPI for HappyRobot Use Case Flow

## To access HappyRobot Deployment:

  - Go to `https://willhappyrobot.ddns.net:3001`

## To Reproduce Deployment:

Prerequisites:
  - EC2 instance running Amazon Linux 2 or 2023
  - SSH access to the instance
  - Domain pointing to your EC2 (e.g., willhappyrobot.ddns.net)

### Steps:

1. SSH into your EC2 Instance:

    `ssh -i <YOUR_KEY.pem> ec2-user@<EC2_PUBLIC_IP>`
   
2. Install Git and Clone the repo and add Certs for Lets Encrypt:

    ```bash
    sudo yum install -y git
    cd ~
    git clone https://github.com/wschmutz123/HappyRobot_CaseStudy.git
    cd HappyRobot_CaseStudy
    mkdir -p Backend/certs
    sudo amazon-linux-extras enable epel
    sudo yum install -y certbot
    
    # Replace willhappyrobot.ddns.net with your domain if you want a different one
    sudo certbot certonly --standalone -d willhappyrobot.ddns.net

    # Replace domain if you have a different domain
    cp /etc/letsencrypt/live/willhappyrobot.ddns.net/fullchain.pem Backend/certs/fullchain.pem
    cp /etc/letsencrypt/live/willhappyrobot.ddns.net/privkey.pem Backend/certs/privkey.pem
   
3. Create .env file with REST API key and WEB TOKEN for your FMCSA api:
   
   ```bash
   cd ~/HappyRobot_CaseStudy/Backend
   touch .env
   echo "REST_API_KEY=<YOUR_SECRET_KEY>" > .env
   echo "WEB_TOKEN=<YOUR_WEB_TOKEN>" > .env

4. Make deploy.sh executable and run the deployment Script:
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


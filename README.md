# HappyRobot_CaseStudy

## FastAPI for HappyRobot Use Case Flow

## To access HappyRobot Deployment:

Prerequisites:
  - EC2 instance running Amazon Linux 2 or 2023
  - SSH access to the instance
  - Domain pointing to your EC2 (e.g., willhappyrobot.ddns.net)

### Steps:

1. SSH into your EC2 Instance:

    `ssh -i <YOUR_KEY.pem> ec2-user@<EC2_PUBLIC_IP>`
   
2. Clone the repo:

    ```bash
    cd ~
    git clone <YOUR_REPO_URL> HappyRobot_CaseStudy
   
3. Create .env file with REST API key:
   
   ```bash
   cd ~/HappyRobot_CaseStudy/Backend
   touch .env
   echo "REST_API_KEY=<YOUR_SECRET_KEY>" > .env

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
   
  URL: https://willhappyrobot.ddns.net:3001 (or EC2 public IP)

  API Key Header: X-API-Key: <YOUR_SECRET_KEY>

  Example:

  ```bash
  curl -H "X-API-Key: <YOUR_SECRET_KEY>" \
  "https://willhappyrobot.ddns.net:3001/api/search_loads?origin=Dallas"
  ```

Notes:
  - Ensure ports 3001 (API) and 80 (HTTP for Let's Encrypt) are open in your EC2 security group.
  - Recommended to use a domain with Let’s Encrypt for HTTPS; self-signed certificates are suitable   for testing only.
  - The deployment script is idempotent, so running it multiple times won’t break your app.


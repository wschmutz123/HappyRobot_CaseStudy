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

4. Make deploy.sh executable in HappyRobot Directory
  `chmod +x deploy.sh`

5. Run the deployment Script:
  `./deploy.sh`
  
This will:

- Install system dependencies (Python 3, pip, git, npm, Certbot)
- Clone the repository
- Set up Python virtual environment and install dependencies
- Make start.sh executable and start the FastAPI app with PM2
- Configure PM2 to auto-start on server reboot

6. Access the API:
   URL: https://willhappyrobot.ddns.net:3001 (or EC2 public IP)

  API Key Header: X-API-Key: <YOUR_SECRET_KEY>

  Example:

  `curl -H "X-API-Key: <YOUR_SECRET_KEY>" \
  "https://willhappyrobot.ddns.net:3001/api/search_loads?origin=Dallas"`

Access the API:
- URL: https://willhappyrobot.ddns.net:3001 (or EC2 public IP)
- API key required: X-API-Key: <YOUR_SECRET_KEY>
`curl -H "X-API-Key: <YOUR_SECRET_KEY>" "https://willhappyrobot.ddns.net:3001/api/search_loads?origin=Dallas"`


# HappyRobot_CaseStudy

## API for HappyRobot Use Case Flow

## To access HappyRobot Deployment:

Prerequisites:
  - EC2 instance running Amazon Linux 2 or 2023
  - SSH access to the instance
  - Domain pointing to your EC2 (e.g., willhappyrobot.ddns.net)

Make deploy.sh executable:
  `cd ~/HappyRobot_CaseStudy/Backend`
  `chmod +x deploy.sh`

Before running the deployment script, you **must create a `.env` file** in the `Backend` directory containing your API key:
1. Create `.env` in the `Backend` directory:
`cd ~/HappyRobot_CaseStudy/Backend`
`touch .env`
Add your REST API key to .env:
`echo "REST_API_KEY=<YOUR_SECRET_KEY>" > .env`

Run the deployment script:
  `./deploy.sh`

This will:
- Install system dependencies (Python 3, pip, git, npm, Certbot)
- Clone the repository
- Set up Python virtual environment and install dependencies
- Make start.sh executable and start the FastAPI app with PM2
- Configure PM2 to auto-start on server reboot

Access the API:
- URL: https://willhappyrobot.ddns.net:3001 (or EC2 public IP)
- API key required: X-API-Key: <YOUR_SECRET_KEY>
`curl -H "X-API-Key: <YOUR_SECRET_KEY>" "https://willhappyrobot.ddns.net:3001/api/search_loads?origin=Dallas"`


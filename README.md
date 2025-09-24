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
    ```bash
     ssh -i <YOUR_KEY.pem> ec2-user@<EC2_PUBLIC_IP>
    ```

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
   
3. Create .env file with REST API key and WEB TOKEN for your FMCSA api:
   
   ```bash
   cd ~/HappyRobot_CaseStudy/Backend
   touch .env
   echo "REST_API_KEY=<YOUR_SECRET_KEY>" > .env
   echo "WEB_TOKEN=<YOUR_WEB_TOKEN>" > .env

4. Make sure the directory contains:

    ```bash
    Backend/
      │── Dockerfile
      │── docker-compose.yml
      │── nginx.conf
      │── app/ (your FastAPI app)
      │── requirements.txt
      |── main.py

5. (Optional) Update your nginx.conf and docker-compose.yml file

    - Update your nginx conf to change the domain name for server_name (twice), ssl_certificate, and ssl_certificate_key
    - Update the entrypoint in docker-compose.yml to your domain and your email 

6. Generate SSL certificates:
   Start Nginx first (HTTP only):
   ```bash
   docker-compose up -d nginx

  Request certificates with Certbot (change your domain if necessary):
  ```bash
    docker-compose run --rm certbot certonly --webroot \
    --webroot-path=/var/www/certbot \
    -d willhappyrobot.ddns.net

    # Make ec2-user the owner
    sudo chown -R ec2-user:ec2-user ./certbot/conf

    # Ensure read permission for Docker
    chmod -R 755 ./certbot/conf
  ```

  Make sure you see certbot directory created in the Backend folder.
  
  After success, reload Nginx with HTTPS:

  ```bash
    docker-compose up -d --force-recreate nginx
  ```

7. Run the stack:
    To start everything:

    `docker-compose up -d`

    Now your FastAPI app should be live at your domain:
   
    `https://willhappyrobot.ddns.net.com`


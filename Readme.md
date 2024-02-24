# Installtion & Creation of CI-CD Pipeline

## Installtions of Packages 
```bash
# Update System Packages
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install docker.io -y

#Install Docker Compose
sudo apt install docker-compose -y

```

## Cloning the GitHub Repository 
- Before Cloning Private Repo following should be done

1. Generate SSH Key from terminal to add it to the GitHub Settings 
```bash 
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

2. Add SSH key to the SSH agent:
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
```

3. Copy the SSH public key to your clipboard:
```bash
cat ~/.ssh/id_rsa.pub
```

- Add SSH Key to GitHub:
1. Copy the SSH public key:
2. Copy the output of the cat ~/.ssh/id_rsa.pub command.

- Move to GitHub Repository:

1. Navigate to your GitHub repository.
2. Go to "Settings" > "Deploy keys" > "Add deploy key."
3. Paste the SSH public key and give it a title.

4. To set your GitHub username and email locally on your development machine, you can use the following Git commands:
- Set User Name:
```bash
git config --global user.name "Your GitHub Username"
```
- Set Email:
```bash
git config --global user.email "your.email@example.com"
```

5. Clone Your GitHub Repository:
```bash 
git clone https://github.com/yourusername/yourrepository.git
```

## Deploy FastAPI Application on VPS:
1. Navigate to Your Project Directory:
```bash 
cd yourrepository
```

2. Follow the current project tree for the more clarity.

3. Build and Run Docker Containers:
```bash
docker-compose up -d --build
```

## Configure Nginx (Optional):
1. Install Nginx:
```bash 
sudo apt install nginx -y
```

2. Add the following configuration (replace your_domain_or_ip with your VPS IP or domain):
```bash
server {
    listen 80;
    server_name your_domain_or_ip;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

3. Create a Symbolic Link:
```bash
sudo ln -s /etc/nginx/sites-available/fastapi /etc/nginx/sites-enabled
```

4. Restart Nginx:
```bash
sudo service nginx restart
```

## Setup GitHub Actions for CI/CD:
1. Create GitHub Actions Workflow:
- Inside your GitHub repository, create a .github/workflows/main.yml file.

```bash
name: CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v2

      - name: Build and Push Docker Image
        run: |
          docker build -t your_docker_username/yourrepository:latest .
          docker login -u your_docker_username -p ${{ secrets.DOCKER_PASSWORD }}
          docker push your_docker_username/yourrepository:latest

      - name: SSH into VPS and Deploy
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USERNAME }}
          key: ${{ secrets.VPS_SSH_KEY }}
          port: 22
          script: |
            cd yourrepository
            git pull origin main
            docker-compose down
            docker-compose up -d --build
```

- Make sure to replace placeholders like your_docker_username, yourrepository, secrets.DOCKER_PASSWORD, secrets.VPS_HOST, secrets.VPS_USERNAME, and secrets.VPS_SSH_KEY with your actual values.

- GitHub Repository Secrets:
  - Go to your GitHub repository.
  - Navigate to "Settings" > "Secrets" > "New repository secret."
  - Add the following secrets:
  - DOCKER_PASSWORD: Your Docker Hub password.
  - VPS_HOST: Your VPS IP address.
  - VPS_USERNAME: Your VPS username.
  - VPS_SSH_KEY: Your private SSH key for connecting to your VPS.
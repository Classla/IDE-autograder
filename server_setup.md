sudo apt-get update # For Ubuntu
sudo apt-get install python3 python3-pip -y
sudo apt-get install git -y
sudo pip3 install virtualenv

sudo apt-get install \
 apt-transport-https \
 ca-certificates \
 curl \
 software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
 "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
 $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io -y
sudo usermod -aG docker $USER
newgrp docker

sudo apt install python3.12-venv
python3 -m venv autograder_env
source autograder_env/bin/activate
pip install -r requirements.txt

sudo apt-get install nginx -y
sudo nano /etc/nginx/sites-available/fastapi

server {
listen 80;
server_name your-ec2-public-dns;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

}

sudo ln -s /etc/nginx/sites-available/fastapi /etc/nginx/sites-enabled
sudo nginx -t # Test the configuration
sudo systemctl restart nginx

sudo nano /etc/systemd/system/fastapi.service

[Unit]
Description=FastAPI application
After=network.target

[Service]
User=ec2-user
Group=www-data
WorkingDirectory=/home/ec2-user/your-repo
ExecStart=/home/ec2-user/your-repo/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target

sudo systemctl start fastapi
sudo systemctl enable fastapi

uvicorn app.main:app --host 0.0.0.0 --port 8000

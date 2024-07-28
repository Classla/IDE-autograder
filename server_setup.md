Set up repository and virtual environement

```
sudo apt-get update
sudo apt-get install python3 python3-pip -y
sudo apt-get install git -y
git clone git@github.com:Classla/IDE-autograder.git
cd IDE-autograder
sudo apt install python3.12-venv
python3 -m venv autograder_env
source autograder_env/bin/activate
pip install -r requirements.txt
```

Install docker

```
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
```

Set up nginx reverse proxy

```

sudo apt-get install nginx -y
sudo nano /etc/nginx/sites-available/fastapi
```

```
server {
listen 80;
server_name autograder.classla.org;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

}
```

```
sudo ln -s /etc/nginx/sites-available/fastapi /etc/nginx/sites-enabled
sudo nginx -t # Test the configuration
sudo systemctl restart nginx
sudo nano /etc/systemd/system/fastapi.service

```

```
[Unit]
Description=FastAPI application
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/IDE-autograder
ExecStart=/home/ubuntu/IDE-autograder/autograder_env/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target

```

Get ssl cert and start API

```

sudo apt-get install certbot python3-certbot-nginx -y
sudo certbot --nginx
sudo nginx -t # Test the Nginx configuration
sudo systemctl reload nginx
sudo systemctl start fastapi
sudo systemctl enable fastapi

```

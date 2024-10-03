
# Get ssl cert and start API

sudo apt-get install certbot python3-certbot-nginx -y
sudo certbot --nginx
sudo nginx -t # Test the Nginx configuration
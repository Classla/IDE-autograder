# IDE-Autograder

## This is an autograder.

Repo configurations:

- [pylint](.pylintrc) (linting)
- unittest (unit testing)

## Running Locally

### Install Dependencies.

```bash
pip install -r requirements.txt # In the repository directory
```

### Build all docker containers.

```bash
for dockerfile in $(ls dockerfiles/); do
    image_name=$(basename $dockerfile | tr '[:upper:]' '[:lower:]')
    docker build -f dockerfiles/$dockerfile -t $image_name .
done
```

### Start the FastAPI server.

```bash
uvicorn app.main:app --reload
```

## Deploying to EC2

1. Start an EC2 instance.
2. Update the following secret variables:

`secrets.EC2_SSH_PRIVATE_KEY` - SHH Private Key for server instance.
`secrets.SSH_HOST` - IP Address or FQDN of server

3. Run `ci-cd.yaml` script once. This is for initial environment setup.

4. SSL cert - Run the following on the server:

```bash
sudo apt-get install certbot python3-certbot-nginx -y
sudo certbot --nginx
sudo nginx -t
```

Note: Future deployments will automatically restart the cert.

## License

This repository is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/) (CC BY-NC-SA 4.0).

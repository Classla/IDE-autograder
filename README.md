# IDE-Autograder

## This is an autograder.

Repo configurations:

- [pylint](.pylintrc) (linting)
- unittest (unit testing)

## Running Locally

### Install Dependencies.

```sh
pip install -r requirements.txt
```

### Build all docker containers.

```bash
for dockerfile in $(ls dockerfiles/); do
    image_name=$(basename $dockerfile | tr '[:upper:]' '[:lower:]')
    docker build -f dockerfiles/$dockerfile -t $image_name .
done
```

### Start the FastAPI server.

```sh
uvicorn app.main:app --reload
```

## Deploying

secrets.EC2_SSH_PRIVATE_KEY
secrets.SSH_HOST

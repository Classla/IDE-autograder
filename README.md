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

## Deploying to EC2

1. Start an EC2 instance.
2. add ssh key TODO
3. Update the following secret variables:

```secrets.EC2_SSH_PRIVATE_KEY
secrets.SSH_HOST
```

4. SSL cert TODO

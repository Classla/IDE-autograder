# Remove pre-existing images
docker image prune -a -f

# Rebuild all docker images
for dockerfile in ./dockerfiles/*; do
    # Get the directory name (context) from the Dockerfile path
    context=$(dirname "$dockerfile")
    # Build the Docker image using the Dockerfile and the context
    docker build -f "$dockerfile" -t $(basename "$dockerfile" .Dockerfile | tr '[:upper:]' '[:lower:]') "$context"
done
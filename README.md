# IDE-Autograder

### This is an autograder.

Repo configurations:

- [pylint](.pylintrc) (linting)
- unittest (unit testing)

Python non-native modules are specified in [requirements.txt](requirements.txt)

Code and Sample Input produce Student.
Student and Expected produce Diff.

Running the API for development:

```
uvicorn app.main:app --reload
```

### Building Docker Images Locally

```bash
for dockerfile in $(ls dockerfiles/); do
    image_name=$(basename $dockerfile | tr '[:upper:]' '[:lower:]')
    docker build -f dockerfiles/$dockerfile -t $image_name .
done
```

TODO: how to build docker image on other machines
TODO: delete orphan containers after script exits.

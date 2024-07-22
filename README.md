# IDE-Autograder

### This is an autograder.

Repo configurations:

- [pylint](.pylintrc) (linting)
- unittest (unit testing)

Python non-native modules are specified in [requirements.txt](requirements.txt)

Terms:
Student - Student output
Expected - Expected output
Code - Student code
Sample Input
Diff - difference file

Code and Sample Input produce Student.
Student and Expected produce Diff.

Running the API for development:

```
uvicorn app.main:app --reload
```

TODO: how to build docker image on other machines
TODO: delete orphan containers after script exits.

## EC2 Deployment steps

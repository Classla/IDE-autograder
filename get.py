# pylint: disable=all

import requests
import json

# Define the URL of the FastAPI endpoint
URL = "http://localhost:8000"

# Send a GET request to the FastAPI endpoint
response = requests.get(URL, timeout=10)

# Print the response from the server
print(json.dumps(response.json(), indent=4))

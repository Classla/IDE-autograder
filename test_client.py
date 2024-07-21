# pylint: disable=all

import requests
from test_resources.sample_request_bodies import input_output, unit_test
import json

# Define the URL of the FastAPI endpoint
URL = "http://localhost:8000/unit_test/"

# Send a POST request to the FastAPI endpoint
response = requests.post(URL, json=unit_test, timeout=10)

# Print the response from the server
print(json.dumps(response.json(), indent=4))

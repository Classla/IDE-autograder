import requests
from test_resources.sample_request_bodies import input_output

# Define the URL of the FastAPI endpoint
url = "http://localhost:8000/input_output/"

# Send a POST request to the FastAPI endpoint
response = requests.post(url, json=input_output)

# Print the response from the server
print(response.json())

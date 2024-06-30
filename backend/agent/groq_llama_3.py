import requests

def get_query_from_user(prompt_text):
  # Define the endpoint and the data payload
  url = "http://localhost:8001/reply"
  data = {"prompt": prompt_text}
  headers = {"Content-Type": "application/json" }
  # Make the POST request
  response = requests.post(url, json=data, headers=headers)
  return response
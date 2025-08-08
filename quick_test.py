import requests
import json

# Quick test of the updated API
url = "http://localhost:8000/hackrx/run"
headers = {
    "Authorization": "Bearer cfe5d188df2d481cbc3d03128a7a93889df967f6c24be452005b2437b7f7b26a",
    "Content-Type": "application/json"
}

data = {
    "documents": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
    "questions": ["What is this document about?"]
}

try:
    response = requests.post(url, json=data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

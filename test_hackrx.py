import requests
import json

# Test script for HackRX API format
def test_hackrx_api():
    base_url = "http://localhost:8000"
    headers = {
        "Authorization": "Bearer cfe5d188df2d481cbc3d03128a7a93889df967f6c24be452005b2437b7f7b26a",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Test health endpoint
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
    
    # Test HackRX health endpoint
    print("\nTesting HackRX health endpoint...")
    try:
        response = requests.get(f"{base_url}/hackrx/health")
        print(f"HackRX health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"HackRX health check failed: {e}")
    
    # Test the main submission endpoint
    print("\nTesting /hackrx/run endpoint...")
    try:
        payload = {
            "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
            "questions": [
                "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
                "What is the waiting period for pre-existing diseases (PED) to be covered?",
                "Does this policy cover maternity expenses, and what are the conditions?",
                "What is the waiting period for cataract surgery?",
                "Are the medical expenses for an organ donor covered under this policy?"
            ]
        }
        
        response = requests.post(f"{base_url}/hackrx/run", json=payload, headers=headers)
        print(f"Submission endpoint: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Number of answers: {len(result['answers'])}")
            for i, answer in enumerate(result['answers']):
                print(f"  A{i+1}: {answer}")
        else:
            print(f"Error response: {response.text}")
            
    except Exception as e:
        print(f"Submission endpoint test failed: {e}")

    # Test without authentication (should fail)
    print("\nTesting without authentication (should fail)...")
    try:
        payload = {
            "documents": "https://example.com/test.pdf",
            "questions": ["What is this about?"]
        }
        
        response = requests.post(f"{base_url}/hackrx/run", json=payload)
        print(f"No auth test: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"No auth test failed: {e}")

if __name__ == "__main__":
    test_hackrx_api()

import requests
import json
import base64

# Simple test script for the simplified API
def test_api():
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
    
    # Test API health endpoint
    print("\nTesting API health endpoint...")
    try:
        response = requests.get(f"{base_url}/api/v1/health")
        print(f"API health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"API health check failed: {e}")
    
    # Test process endpoint with dummy data
    print("\nTesting process endpoint...")
    try:
        # Create dummy PDF blob (just some base64 encoded text for testing)
        dummy_pdf = base64.b64encode(b"This is a test PDF content").decode('utf-8')
        
        payload = {
            "pdf_blob": dummy_pdf,
            "questions": [
                "What is this document about?",
                "What are the key points?"
            ]
        }
        
        response = requests.post(f"{base_url}/api/v1/process", json=payload)
        print(f"Process endpoint: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Request ID: {result['request_id']}")
            print(f"Processing time: {result['processing_time_ms']}ms")
            print(f"Number of results: {len(result['results'])}")
            for i, result_item in enumerate(result['results']):
                print(f"  Q{i+1}: {result_item['question']}")
                print(f"  A{i+1}: {result_item['answer'][:100]}...")
        else:
            print(f"Error response: {response.text}")
            
    except Exception as e:
        print(f"Process endpoint test failed: {e}")

if __name__ == "__main__":
    test_api()

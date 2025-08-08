#!/usr/bin/env python3
"""
Test the updated HackRX API with actual PDF processing
"""
import requests
import json

# API configuration
BASE_URL = "http://localhost:8000"
TOKEN = "cfe5d188df2d481cbc3d03128a7a93889df967f6c24be452005b2437b7f7b26a"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def test_debug_endpoint():
    """Test the debug endpoint to see PDF processing"""
    print("🔍 Testing Debug Endpoint...")
    
    # Test with a sample PDF URL (you can replace this)
    test_data = {
        "documents": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
        "questions": ["What is this document about?", "What are the main topics?"]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/hackrx/debug", json=test_data, headers=HEADERS)
        response.raise_for_status()
        
        result = response.json()
        print("✅ Debug Response:")
        print(f"   PDF Size: {result.get('pdf_size_bytes', 0)} bytes")
        print(f"   Text Length: {result.get('extracted_text_length', 0)} characters")
        print(f"   Preview: {result.get('extracted_preview', 'No preview')[:200]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Debug test failed: {e}")
        return False

def test_main_endpoint():
    """Test the main processing endpoint"""
    print("\n🎯 Testing Main Endpoint...")
    
    test_data = {
        "documents": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
        "questions": [
            "What is the grace period?",
            "What are the waiting periods?", 
            "What is covered under maternity?"
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/hackrx/run", json=test_data, headers=HEADERS)
        response.raise_for_status()
        
        result = response.json()
        print("✅ Main Response:")
        for i, answer in enumerate(result.get('answers', []), 1):
            print(f"   Q{i}: {answer[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Main test failed: {e}")
        return False

def test_health_check():
    """Test health endpoint"""
    print("\n❤️ Testing Health Check...")
    
    try:
        response = requests.get(f"{BASE_URL}/hackrx/health")
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Health: {result.get('status', 'unknown')}")
        return True
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Updated HackRX API with PDF Processing\n")
    
    # Run all tests
    tests_passed = 0
    total_tests = 3
    
    if test_health_check():
        tests_passed += 1
    
    if test_debug_endpoint():
        tests_passed += 1
        
    if test_main_endpoint():
        tests_passed += 1
    
    print(f"\n📊 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your API is now processing actual PDF content!")
    else:
        print("⚠️ Some tests failed. Check the error messages above.")

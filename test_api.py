#!/usr/bin/env python
import time
import requests
import json

print("Waiting for server to start...")
time.sleep(2)

# Test the server
try:
    # Test the /test endpoint
    print("\n1. Testing /test endpoint...")
    response = requests.get('http://127.0.0.1:8000/test', timeout=5)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test the /health endpoint
    print("\n2. Testing /health endpoint...")
    response = requests.get('http://127.0.0.1:8000/health', timeout=5)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test the /stats endpoint
    print("\n3. Testing /stats endpoint...")
    response = requests.get('http://127.0.0.1:8000/stats', timeout=5)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test the root endpoint
    print("\n4. Testing / (root) endpoint...")
    response = requests.get('http://127.0.0.1:8000/', timeout=5)
    print(f"Status Code: {response.status_code}")
    # print(f"Response preview: {response.text[:200]}...")
    
    print("\n✅ All basic endpoints are working!")
    
except requests.exceptions.ConnectionError as e:
    print(f"❌ Connection Error: {e}")
    print("Server may not be running.")
except requests.exceptions.RequestException as e:
    print(f"❌ Request Error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

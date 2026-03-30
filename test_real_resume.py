import requests

# Test the endpoint with actual resume file
url = "http://127.0.0.1:8000/analyze"
files = {'resume_file': open('sample_resume.pdf', 'rb')}

try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("✓ Analysis successful!")
        data = response.json()
        print(f"Score: {data['score']}")
        print(f"Sections found: {data['sections_found']}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {e}")

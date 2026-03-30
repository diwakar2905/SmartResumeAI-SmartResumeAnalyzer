import requests

# Test with Diwakar's resume that was causing the error
url = "http://127.0.0.1:8000/analyze"
files = {'resume_file': open('DIWAKAR MISHRA_Artificial Intelligence Intern_20250728.pdf', 'rb')}

try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("✓ Analysis successful!")
        data = response.json()
        print(f"Score: {data['score']}")
        print(f"Sections found: {data['sections_found']}")
        print(f"Skills categories: {list(data['skills'].keys())}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {e}")

#!/usr/bin/env python
"""Test the /analyze endpoint with existing sample resume"""
import requests
import time
import json

print("Waiting for server to be ready...")
time.sleep(1)

print("\nTesting /analyze endpoint with sample resume...\n")

try:
    url = "http://127.0.0.1:8000/analyze"
    
    # Use the existing sample_resume.pdf
    with open('sample_resume.pdf', 'rb') as f:
        files = {'resume_file': f}
        response = requests.post(url, files=files, timeout=15)
    
    print(f"Status Code: {response.status_code}\n")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ SUCCESS: Resume analyzed successfully!\n")
        
        skills = data.get('skills', {})
        print(f"Total Skills Found: {data['analysis_metadata']['text_length']} characters processed")
        
        print("\nSkills by Category:")
        for category, skill_list in skills.items():
            if skill_list:
                print(f"\n  {category}:")
                for skill in skill_list[:5]:  # Show first 5 skills
                    print(f"    - {skill}")
                if len(skill_list) > 5:
                    print(f"    ... and {len(skill_list) - 5} more")
        
        print(f"\n\nResume Score: {data.get('score', 'N/A')}")
        if data.get('basic_info'):
            print(f"Name: {data['basic_info'].get('name', 'N/A')}")
        
    else:
        print(f"❌ Error {response.status_code}:")
        print(f"Response: {response.text}")
        
except FileNotFoundError:
    print("❌ sample_resume.pdf not found")
except requests.exceptions.ConnectionError as e:
    print(f"❌ Connection Error: Server may not be running")
except requests.exceptions.Timeout:
    print(f"❌ Request timeout - server took too long")
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

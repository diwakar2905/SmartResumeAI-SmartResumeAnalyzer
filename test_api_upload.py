#!/usr/bin/env python
"""Test the /analyze endpoint with a sample resume"""
import requests
import io
import time
import json

# Simple PDF with skill-containing text
pdf_content = b"""%PDF-1.4
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R/Resources<</Font<</F1<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>>>>>endobj
4 0 obj<</Length 500>>stream
BT
/F1 14 Tf
50 750 Td
(John Doe - Senior Software Engineer) Tj
0 -20 Td
(SKILLS) Tj
0 -15 Td
/F1 12 Tf
(Programming: Python, Java, JavaScript) Tj
0 -12 Td
(Frontend: React, Vue.js, HTML5, CSS3, Tailwind CSS) Tj
0 -12 Td
(Backend: Node.js, Express, Django, Flask, PostgreSQL, MongoDB) Tj
0 -12 Td
(Cloud: AWS, Docker, Kubernetes) Tj
0 -12 Td
(EXPERIENCE) Tj
0 -15 Td
(Senior Backend Engineer - Tech Company 2020-Present) Tj
0 -12 Td
(Built scalable APIs using Node.js and Express) Tj
0 -12 Td
(Managed PostgreSQL databases) Tj
0 -12 Td
(Deployed on AWS with Docker and Kubernetes) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000273 00000 n
trailer<</Size 5/Root 1 0 R>>
startxref
823
%%EOF
"""

print("Waiting for server to be ready...")
time.sleep(1)

print("\nTesting /analyze endpoint with sample resume PDF...\n")

try:
    url = "http://127.0.0.1:8000/analyze"
    files = {'resume_file': ('sample_resume.pdf', io.BytesIO(pdf_content))}
    
    response = requests.post(url, files=files, timeout=10)
    
    print(f"Status Code: {response.status_code}\n")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ SUCCESS: Resume analyzed successfully!\n")
        
        print("Skills by Category:")
        for category, skills in data.get('skills', {}).items():
            if skills:
                print(f"\n  {category}:")
                for skill in skills[:5]:  # Show first 5 skills
                    print(f"    - {skill}")
        
        print(f"\n\nResume Score: {data.get('score', 'N/A')}")
        print(f"File Name: {data.get('basic_info', {}).get('name', 'N/A')}")
        
    else:
        print(f"❌ Error {response.status_code}:")
        print(f"Response: {response.text}")
        
except requests.exceptions.ConnectionError as e:
    print(f"❌ Connection Error: Server may not be running")
    print(f"Error: {e}")
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

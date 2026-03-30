import requests
import io

# Create a simple test PDF file
test_pdf_content = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj 2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj 3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R/Resources<</Font<</F1<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>>>>>endobj 4 0 obj<</Length 44>>stream BT /F1 12 Tf 100 700 Td (John Doe) Tj ET endstream endobj xref 0 5 0000000000 65535 f 0000000009 00000 n 0000000058 00000 n 0000000115 00000 n 0000000273 00000 n trailer<</Size 5/Root 1 0 R>> startxref 366 %%EOF"

# Test the endpoint
url = "http://127.0.0.1:8000/analyze"
files = {'resume_file': ('test_resume.pdf', io.BytesIO(test_pdf_content))}

try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

#!/usr/bin/env python3
"""
Update script for deployment to Render + Vercel
This script helps update all necessary URLs and configurations for production deployment
"""

import os
import sys

def update_index_html(backend_url):
    """Update the backend URL in index.html"""
    index_path = "templates/index.html"
    
    if not os.path.exists(index_path):
        print(f"❌ {index_path} not found")
        return False
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace localhost with production URL
    original = 'const BACKEND_BASE_URL = "http://127.0.0.1:8000";'
    updated = f'const BACKEND_BASE_URL = "{backend_url}";'
    
    if original in content:
        content = content.replace(original, updated)
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Updated {index_path}")
        print(f"   Backend URL: {backend_url}")
        return True
    else:
        print(f"⚠️  Could not find BACKEND_BASE_URL in {index_path}")
        return False

def update_output_html(backend_url):
    """Update the backend URL in output.html"""
    output_path = "templates/output.html"
    
    if not os.path.exists(output_path):
        print(f"⚠️  {output_path} not found (this is optional)")
        return True
    
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for any localhost references
    if "localhost" in content or "127.0.0.1" in content:
        # Replace common patterns
        content = content.replace("http://127.0.0.1:8000", backend_url)
        content = content.replace("http://localhost:8000", backend_url)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Updated {output_path}")
        return True
    
    return False

def update_render_yaml(frontend_url):
    """Update CORS_ORIGINS in render.yaml"""
    render_yaml_path = "render.yaml"
    
    if not os.path.exists(render_yaml_path):
        print(f"⚠️  {render_yaml_path} not found")
        return False
    
    with open(render_yaml_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Note: CORS should be set as environment variable, not in file
    print(f"⚠️  Set CORS_ORIGINS environment variable in Render dashboard to:")
    print(f"   {frontend_url}")
    
    return True

def main():
    print("=" * 60)
    print("Smart Resume Analyzer - Deployment URL Update Script")
    print("=" * 60)
    print()
    
    # Get URLs from user
    backend_url = input("Enter your Render backend URL (e.g., https://smart-resume-api.onrender.com): ").strip()
    frontend_url = input("Enter your Vercel frontend URL (e.g., https://smart-resume.vercel.app): ").strip()
    
    if not backend_url or not frontend_url:
        print("❌ Both URLs are required!")
        return False
    
    print()
    print("Updating files...")
    print()
    
    # Update files
    success = True
    success = update_index_html(backend_url) and success
    success = update_output_html(backend_url) and success
    success = update_render_yaml(frontend_url) and success
    
    print()
    print("=" * 60)
    print("Post-Update Checklist:")
    print("=" * 60)
    print()
    print("1. ✅ Frontend URLs updated to:", backend_url)
    print()
    print("2. 🔧 Set Backend Environment Variables on Render:")
    print(f"   CORS_ORIGINS = {frontend_url}")
    print()
    print("3. 🚀 Deploy to GitHub:")
    print("   git add .")
    print("   git commit -m 'Update URLs for production deployment'")
    print("   git push origin main")
    print()
    print("4. ✅ Render will auto-deploy when you push")
    print("5. ✅ Vercel will auto-deploy when you push")
    print()
    print("5. 🧪 Test your application:")
    print(f"   Frontend: {frontend_url}")
    print(f"   API Docs: {backend_url}/docs")
    print()
    print("=" * 60)
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

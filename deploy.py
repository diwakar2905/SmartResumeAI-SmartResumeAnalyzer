#!/usr/bin/env python3
"""
Deployment script for Smart Resume Analyzer
Handles production setup, server management, and deployment tasks.
"""

import os
import sys
import subprocess
import shutil
import venv
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None

def setup_virtual_environment():
    """Create and activate a virtual environment."""
    print("📦 Setting up virtual environment...")
    venv_dir = Path("venv")
    if not venv_dir.exists():
        venv.create(venv_dir, with_pip=True, symlinks=True)
        print(f"✅ Virtual environment created at {venv_dir}")
    else:
        print(f"✅ Virtual environment already exists at {venv_dir}")
    
    # Set up environment for subsequent commands
    os.environ['VIRTUAL_ENV'] = str(venv_dir.resolve())
    os.environ['PATH'] = str(venv_dir.resolve() / "bin") + os.pathsep + os.environ['PATH']
    print("✅ Virtual environment activated for script execution.")

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'fastapi', 'uvicorn', 'python-multipart', 'pymupdf', 'python-docx',
        'spacy', 'werkzeug', 'gunicorn', 'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            # Try importing within the current (potentially venv-activated) environment
            subprocess.run([sys.executable, "-c", f"import {package.replace('-', '_')}"], check=True, capture_output=True)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("📦 Installing missing packages...")
        run_command(f"pip install {' '.join(missing_packages)}", "Installing packages")
    elif Path("requirements.txt").exists(): # Also install from requirements.txt if it exists
        print("✅ All dependencies are installed")

def setup_directories():
    """Create necessary directories."""
    print("📁 Setting up directories...")
    
    directories = [
        'temp_uploads',
        'logs',
        'static',
        'templates'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
def setup_environment():
    """Set up environment variables."""
    print("🌍 Setting up environment...")
    
    env_content = """# Smart Resume Analyzer Environment Variables
# Change these values for production

# FastAPI Configuration (formerly Flask)
SECRET_KEY=your-super-secret-key-change-this-in-production
DEBUG=False
HOST=0.0.0.0
PORT=5001

# Logging
LOG_LEVEL=INFO

# CORS (comma-separated origins)
CORS_ORIGINS=*

# Analysis Configuration
MAX_TEXT_LENGTH=50000
MIN_TEXT_LENGTH=100
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Environment file created: .env")
    print("⚠️  Remember to change SECRET_KEY in production!")

def install_spacy_model():
    """Install spaCy English model."""
    print("🧠 Installing spaCy English model...")
    result = run_command("python -m spacy download en_core_web_sm", "Installing spaCy model")
    if result:
        print("✅ spaCy model installed successfully")
    else:
        print("❌ Failed to install spaCy model")

def create_gunicorn_config():
    """Create Gunicorn configuration for production."""
    print("🐳 Creating Gunicorn configuration...")
    
    gunicorn_config = """# Gunicorn configuration for Smart Resume Analyzer
bind = "0.0.0.0:5001"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
reload = False
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"
capture_output = True
"""
    
    with open('gunicorn.conf.py', 'w') as f:
        f.write(gunicorn_config)
    
    print("✅ Gunicorn configuration created: gunicorn.conf.py")

def create_systemd_service():
    """Create systemd service file for production deployment."""
    print("🔧 Creating systemd service...")
    
    current_dir = os.getcwd()
    service_content = f"""[Unit]
Description=Smart Resume Analyzer
After=network.target

[Service]
Type=notify
User={os.getenv('USER', 'www-data')}
WorkingDirectory={current_dir}
Environment=PATH={current_dir}/venv/bin:{os.environ.get('PATH', '')}
ExecStart={current_dir}/venv/bin/gunicorn --config gunicorn.conf.py app:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
"""
    
    with open('smart-resume-analyzer.service', 'w') as f:
        f.write(service_content)
    
    print("✅ Systemd service file created: smart-resume-analyzer.service")
    print("📋 To install the service, run:")
    print("   sudo cp smart-resume-analyzer.service /etc/systemd/system/")
    print("   sudo systemctl daemon-reload")
    print("   sudo systemctl enable smart-resume-analyzer")
    print("   sudo systemctl start smart-resume-analyzer")

def create_nginx_config():
    """Create Nginx configuration for reverse proxy."""
    print("🌐 Creating Nginx configuration...")
    
    nginx_config = """server {
    listen 80;
    server_name your-domain.com;  # Change this to your domain
    
    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # File upload settings
        client_max_body_size 16M; # Ensure this matches FastAPI's MAX_FILE_SIZE
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
    
    # Serve static files directly
    location /static/ {
        alias /path/to/your/app/static/;
        expires 1y; # Cache static files for a long time
        add_header Cache-Control "public, immutable";
    }
}
"""
    
    with open('nginx.conf', 'w') as f:
        f.write(nginx_config)
    
    print(f"⚠️  Remember to replace 'your-domain.com' and '/path/to/your/app/static/' in nginx.conf!")
    print("✅ Nginx configuration created: nginx.conf")
    print("📋 To use this configuration:")
    print("   1. Copy to /etc/nginx/sites-available/")
    print("   2. Create symlink in sites-enabled/")
    print("   3. Test with: sudo nginx -t")
    print("   4. Reload: sudo systemctl reload nginx")

def run_tests():
    """Run basic tests to ensure everything works."""
    print("🧪 Running basic tests...")
    
    # Test imports
    try:
        import uvicorn
        import spacy
        print("✅ All imports successful")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test spaCy model
    try:
        nlp = spacy.load('en_core_web_sm')
        print("✅ spaCy model loaded successfully")
    except OSError:
        print("❌ spaCy model not found")
        return False
    
    print("✅ All tests passed")
    return True

def main():
    """Main deployment function."""
    print("🚀 Smart Resume Analyzer - Production Deployment")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version} detected")
    
    # Run deployment steps
    setup_virtual_environment()
    check_dependencies()
    setup_directories()
    setup_environment()
    install_spacy_model()
    create_gunicorn_config()
    create_systemd_service()
    create_nginx_config()
    
    # Run tests
    if run_tests():
        print("\n🎉 Deployment setup completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Review and edit .env file")
        print("   2. Test the application: python app.py")
        print("   3. For production deployment:")
        print("      - Copy service file to systemd")
        print("      - Configure Nginx")
        print("      - Set up SSL certificates")
        print("      - Configure firewall")
    else:
        print("\n❌ Deployment setup failed. Please check the errors above.")

if __name__ == "__main__":
    main() 
# 🧠 Smart Resume Analyzer - Production Deployment Guide

This document covers production deployment configurations, infrastructure setup, security considerations, and system verification.

---

## 🛠️ Tech Stack & Production Components

- **Backend Gateway**: FastAPI serving a REST API.
- **Production ASGI Server**: Gunicorn (configured in `gunicorn.conf.py` with 4 Uvicorn ASGI worker processes).
- **Reverse Proxy**: Nginx (configured in `nginx.conf` for reverse proxying to Gunicorn, static asset hosting, caching, and rate limiting limits).
- **Service Management**: systemd service wrapper for process management and automatic restarts.

---

## 🚀 Production Deployment Steps

### 1. Automated Setup
The repository includes a helper deployment script that automates environment setup. To run it:
```bash
python deploy.py
```
This script will:
- Check for system Python dependencies.
- Initialize/activate a local `venv` virtual environment.
- Install packages from `requirements.txt`.
- Download the required spaCy model.
- Generate a default `.env` template.
- Output configuration templates for Nginx and systemd.

### 2. Manual Service Setup (Linux)

#### A. Install Production Packages
Activate your virtual environment and install gunicorn and production variables handler:
```bash
pip install gunicorn python-dotenv
```

#### B. Setup Environment Configuration
Create a `.env` file in the project root:
```env
SECRET_KEY=your-custom-production-secret-key
DEBUG=False
HOST=0.0.0.0
PORT=5001
CORS_ORIGINS=https://yourdomain.com
```

#### C. systemd Service Configuration
1. Copy the systemd service template to the system folder:
   ```bash
   sudo cp smart-resume-analyzer.service /etc/systemd/system/
   ```
2. Reload systemd, enable, and start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable smart-resume-analyzer
   sudo systemctl start smart-resume-analyzer
   ```
3. Check service health:
   ```bash
   sudo systemctl status smart-resume-analyzer
   ```

#### D. Nginx Configuration
1. Copy the Nginx server block configuration to `sites-available`:
   ```bash
   sudo cp nginx.conf /etc/nginx/sites-available/smart-resume-analyzer
   ```
2. Enable the site and restart Nginx:
   ```bash
   sudo ln -s /etc/nginx/sites-available/smart-resume-analyzer /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

---

## 🧪 Verification & Diagnostics

To run the verification test suite:
```bash
python -m unittest test_app.py
```

### Health Check Endpoint
```bash
curl http://127.0.0.1:5001/health
```

### API Performance & Statistics
```bash
curl http://127.0.0.1:5001/stats
```

---

## 🔒 Security Configuration

- **Upload Folder Bounds**: File uploads are capped at 16MB via FastAPI's content length checks.
- **Allowed Formats**: Validates headers and limits extensions to `{'pdf', 'docx'}`.
- **Filename Sanitization**: Sanitizes file uploads using `werkzeug.utils.secure_filename` and appends timestamps to prevent directory traversal or file collision.
- **Immediate Cleanup**: Temporary files are deleted immediately after parsing. If any orphaned file remains, a cleanup job purges files older than 1 hour during requests.
- **CORS Protection**: Access control headers are configured from the `CORS_ORIGINS` environment variable.
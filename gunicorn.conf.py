import os

# Gunicorn configuration for Smart Resume Analyzer
# Bind to the port specified by the PORT environment variable, defaulting to 5001 for local development.
# This is crucial for platforms like Railway and Render.
port = os.environ.get("PORT", "5001")
bind = f"0.0.0.0:{port}"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 120
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
reload = False
accesslog = "-"
errorlog = "-"
loglevel = "info"
capture_output = True

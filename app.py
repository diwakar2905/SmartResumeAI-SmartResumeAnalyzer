import os
import traceback
import logging
from datetime import datetime
import json
import shutil
from typing import List, Dict, Any

from fastapi import FastAPI, Request, File, UploadFile, HTTPException, Response, status
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from werkzeug.utils import secure_filename

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Import core logic functions - Apne existing functions ko import karte hain
from parser.resume_parser import extract_text_from_pdf, extract_text_from_docx, extract_basic_info
from utils.skill_classifier import classify_skills, classify_skills_enhanced
from utils.scoring import score_resume, WEIGHTS
from utils.feedback import generate_feedback, generate_enhanced_feedback
from utils.section_extractor import extract_sections
from utils.report_generator import generate_pdf_report

# Configure logging - Logging setup karte hain taki sab kuch track kar sakein
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize the FastAPI App - FastAPI app ko initialize karte hain
app = FastAPI(title="Smart Resume Analyzer API")

# Configure CORS from environment variables for production security
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')  # Default to '*' for local dev
origins = CORS_ORIGINS.split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info(f"CORS configured for origins: {CORS_ORIGINS}")

# Configuration - App ki configuration set karte hain
UPLOAD_FOLDER = 'temp_uploads'  # Temporary upload folder - Temporary files ke liye folder
ALLOWED_EXTENSIONS = {'pdf', 'docx'}  # Allowed file types
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size - Maximum file size 16MB

# Ensure upload directory exists - Upload folder exist karta hai ya nahi check karte hain
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Mount static and template directories - Static aur templates directories mount karte hain
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def allowed_file(filename):
    """Check if the file's extension is allowed - File ka extension allowed hai ya nahi check karte hain."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleanup_old_files():
    """Clean up files older than 1 hour in temp_uploads - 1 ghante purane files ko delete karte hain."""
    try:
        current_time = datetime.now()
        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                if (current_time - file_time).total_seconds() > 3600:  # 1 hour - 1 ghanta
                    os.remove(filepath)
                    logger.info(f"Cleaned up old file: {filename}")
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")

# Logging middleware - Har request ko log karne ka middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url.path} - {request.client.host if request.client else 'N/A'}")
    response = await call_next(request)
    return response

# Custom Exception Handlers - Custom errors manage karte hain
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"HTTP error {exc.status_code}: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Internal server error: {exc}")
    logger.error(traceback.format_exc())
    return JSONResponse(status_code=500, content={"error": "Internal server error"})

# Serve HTML Templates - HTML page serve karte hain
@app.get('/', response_class=HTMLResponse, name="index")
async def index(request: Request):
    """Serve the main HTML page - Main HTML page serve karte hain."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/about', response_class=HTMLResponse, name="about")
async def about(request: Request):
    """Serve the about page."""
    return templates.TemplateResponse("about.html", {"request": request})

@app.get('/contact', response_class=HTMLResponse, name="contact")
async def contact(request: Request):
    """Serve the contact page."""
    return templates.TemplateResponse("contact.html", {"request": request})

@app.get('/features', response_class=HTMLResponse, name="features")
async def features(request: Request):
    """Serve the features page."""
    return templates.TemplateResponse("features.html", {"request": request})

@app.get('/output', response_class=HTMLResponse, name="output")
async def output(request: Request):
    """Serve the analysis output page."""
    return templates.TemplateResponse("output.html", {"request": request})

@app.post('/api/generate-report')
async def generate_report(data: Dict[str, Any]):
    """Generate a PDF report from analysis data."""
    try:
        if not data:
            raise HTTPException(status_code=400, detail="No analysis data provided")

        logger.info("Generating PDF report...")
        pdf_bytes = generate_pdf_report(data)
        
        filename = data.get("analysis_metadata", {}).get("file_name", "resume")
        report_filename = f"Smart_Resume_Analysis_{filename}.pdf"

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=\"{report_filename}\""}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating PDF report: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate PDF report.")

@app.post('/analyze')
async def analyze_resume(request: Request, resume_file: UploadFile = File(...)):
    """Analyze uploaded resume file - Uploaded resume file ko analyze karte hain."""
    start_time = datetime.now()
    filepath = None
    safe_filename = None
    
    try:
        # Clean up old files - Purane files ko clean up karte hain
        cleanup_old_files()
        
        # Validate request size - Content-Length verify karte hain
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > MAX_CONTENT_LENGTH:
            raise HTTPException(status_code=413, detail="File too large. Maximum size is 16MB.")

        if resume_file.size and resume_file.size > MAX_CONTENT_LENGTH:
            raise HTTPException(status_code=413, detail="File too large. Maximum size is 16MB.")

        if not resume_file.filename:
            raise HTTPException(status_code=400, detail="No file selected")
        
        if not allowed_file(resume_file.filename):
            raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a PDF or DOCX file.")

        # Secure filename and save - Secure filename banate hain aur save karte hain
        filename = secure_filename(resume_file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, safe_filename)
        
        logger.info(f"Processing file: {filename} -> {safe_filename}")
        
        # Save file to disk
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(resume_file.file, buffer)
        
        # Extract text based on file type - File type ke hisab se text extract karte hain
        text = ""
        file_extension = filename.rsplit('.', 1)[1].lower()
        
        if file_extension == 'pdf':
            logger.info("Extracting text from PDF...")
            text = extract_text_from_pdf(filepath)
        elif file_extension == 'docx':
            logger.info("Extracting text from DOCX...")
            text = extract_text_from_docx(filepath)
        
        if not text:
            raise HTTPException(status_code=500, detail="Could not extract text from the file. It might be corrupted, password-protected, or contain only images.")

        logger.info(f"Text extraction successful. Length: {len(text)} characters")
        logger.info("Starting resume analysis...")
        
        # Classify skills with enhanced analysis - Enhanced analysis ke saath skills classify karte hain
        skills_data = classify_skills_enhanced(text)
        skills = skills_data["skills_by_category"]
        skill_count = skills_data["statistics"]["total_skills"]
        avg_confidence = skills_data["statistics"]["average_confidence"]
        logger.info(f"Enhanced skills classified: {skill_count} skills found (avg confidence: {avg_confidence})")
        
        # Extract sections - Sections extract karte hain
        sections = extract_sections(text)
        logger.info(f"Sections found: {sections}")
        
        # Calculate enhanced score with detailed analysis - Enhanced score detailed analysis ke saath calculate karte hain
        score_data = score_resume(sections, WEIGHTS, text)
        score = score_data["overall_score"]
        logger.info(f"Enhanced score calculated: {score} (Grade: {score_data['grade']})")
        
        # Generate enhanced feedback - Enhanced feedback generate karte hain
        feedback = generate_enhanced_feedback(sections, score_data, text)
        logger.info(f"Enhanced feedback generated: {len(feedback)} items")

        # Prepare response - Response prepare karte hain
        response_data = {
            "skills": skills,
            "score": score,
            "feedback": feedback,
            "sections_found": sections,
            "analysis_metadata": {
                "file_name": filename,
                "file_size": os.path.getsize(filepath),
                "text_length": len(text),
                "processing_time": (datetime.now() - start_time).total_seconds(),
                "timestamp": datetime.now().isoformat()
            }
        }
        logger.info("Analysis completed successfully!")
        return response_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred during analysis.")
    finally:
        # Cleanup uploaded file
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
                logger.info(f"Cleaned up file: {safe_filename}")
            except Exception as e:
                logger.error(f"Error cleaning up file: {e}")

@app.get('/test')
async def test_endpoint():
    """Test endpoint to verify server communication."""
    return {
        "status": "success",
        "message": "Server is working correctly",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }

@app.get('/health')
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "Smart Resume Analyzer API is running",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get('/stats')
async def get_stats():
    """Get API statistics."""
    try:
        file_count = len([f for f in os.listdir(UPLOAD_FOLDER) 
                         if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))])
        
        return {
            "status": "success",
            "stats": {
                "temp_files": file_count,
                "max_file_size": "16MB",
                "supported_formats": list(ALLOWED_EXTENSIONS),
                "server_time": datetime.now().isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Could not retrieve statistics")

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    """Serve favicon safely."""
    ico_path = os.path.join('static', 'favicon.ico')
    png_path = os.path.join('static', 'Free.png')
    if os.path.exists(ico_path):
        return FileResponse(ico_path)
    elif os.path.exists(png_path):
        return FileResponse(png_path, media_type="image/png")
    return Response(status_code=204)

if __name__ == '__main__':
    import uvicorn
    logger.info("Starting Smart Resume Analyzer server...")
    port = int(os.environ.get("PORT", 5001))
    host = os.environ.get("HOST", "127.0.0.1")
    logger.info(f"Server will be available at: http://{host}:{port}")
    uvicorn.run("app:app", host=host, port=port, reload=False)
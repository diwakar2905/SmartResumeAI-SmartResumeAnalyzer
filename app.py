import os
import traceback
import logging
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, Request, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import aiofiles
from pathlib import Path
import io

# Import your existing functions
from parser.resume_parser import extract_text_from_pdf, extract_text_from_docx, extract_basic_info
from utils.skill_classifier import classify_skills, classify_skills_enhanced
from utils.scoring import score_resume, WEIGHTS
from utils.feedback import generate_feedback, generate_enhanced_feedback
from utils.section_extractor import extract_sections
from utils.report_generator import generate_pdf_report

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Smart Resume Analyzer API",
    description="Advanced resume parsing and analysis API",
    version="2.0.0"
)

# Configure CORS
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info(f"CORS configured for origins: {CORS_ORIGINS}")

# Configuration
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB max file size
UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Ensure upload directory exists
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)

# Mount static files - Mount static directory
static_path = Path('static')
if static_path.exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")

def allowed_file(filename: str) -> bool:
    """Check if the file's extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

async def cleanup_old_files():
    """Clean up files older than 1 hour in temp_uploads."""
    try:
        current_time = datetime.now()
        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                if (current_time - file_time).total_seconds() > 3600:  # 1 hour
                    os.remove(filepath)
                    logger.info(f"Cleaned up old file: {filename}")
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")

async def delete_file(filepath: str):
    """Delete file asynchronously."""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"Cleaned up file: {filepath}")
    except Exception as e:
        logger.error(f"Error cleaning up file: {e}")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests."""
    logger.info(f"{request.method} {request.url.path} - {request.client}")
    response = await call_next(request)
    return response

@app.get("/", response_class=HTMLResponse)
async def index():
    """Serve the main HTML page."""
    try:
        async with aiofiles.open('templates/index.html', 'r', encoding='utf-8') as f:
            return await f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="index.html not found")

@app.get("/about", response_class=HTMLResponse)
async def about():
    """Serve the about page."""
    try:
        async with aiofiles.open('templates/about.html', 'r', encoding='utf-8') as f:
            return await f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="about.html not found")

@app.get("/contact", response_class=HTMLResponse)
async def contact():
    """Serve the contact page."""
    try:
        async with aiofiles.open('templates/contact.html', 'r', encoding='utf-8') as f:
            return await f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="contact.html not found")

@app.get("/features", response_class=HTMLResponse)
async def features():
    """Serve the features page."""
    try:
        async with aiofiles.open('templates/features.html', 'r', encoding='utf-8') as f:
            return await f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="features.html not found")

@app.get("/output", response_class=HTMLResponse)
async def output():
    """Serve the analysis output page."""
    try:
        async with aiofiles.open('templates/output.html', 'r', encoding='utf-8') as f:
            return await f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="output.html not found")

@app.post("/api/generate-report")
async def generate_report(request: Request, background_tasks: BackgroundTasks):
    """Generate a PDF report from analysis data."""
    try:
        analysis_data = await request.json()
        if not analysis_data:
            raise HTTPException(status_code=400, detail="No analysis data provided")

        logger.info("Generating PDF report...")
        pdf_buffer = generate_pdf_report(analysis_data)
        
        filename = analysis_data.get("analysis_metadata", {}).get("file_name", "resume")
        report_filename = f"Smart_Resume_Analysis_{filename}.pdf"

        return FileResponse(
            io.BytesIO(pdf_buffer),
            media_type="application/pdf",
            filename=report_filename
        )
    except Exception as e:
        logger.error(f"Error generating PDF report: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate PDF report")

@app.post("/analyze")
async def analyze_resume(resume_file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    """Analyze uploaded resume file."""
    start_time = datetime.now()
    filepath = None
    safe_filename = None
    
    try:
        # Clean up old files
        await cleanup_old_files()
        
        # Validate file
        if not resume_file:
            raise HTTPException(status_code=400, detail="No resume file provided")
        
        if not resume_file.filename:
            raise HTTPException(status_code=400, detail="No file selected")
        
        if not allowed_file(resume_file.filename):
            raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a PDF or DOCX file.")

        # Check file size
        file_content = await resume_file.read()
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large. Maximum size is 16MB.")

        # Secure filename and save
        from werkzeug.utils import secure_filename
        filename = secure_filename(resume_file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, safe_filename)
        
        logger.info(f"Processing file: {filename} -> {safe_filename}")
        
        # Save file
        async with aiofiles.open(filepath, 'wb') as f:
            await f.write(file_content)
        
        # Extract text based on file type
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
        
        # Perform analysis
        logger.info("Starting resume analysis...")
        
        # Classify skills with enhanced analysis
        skills_data = classify_skills_enhanced(text)
        skills = skills_data["skills_by_category"]
        skill_count = skills_data["statistics"]["total_skills"]
        avg_confidence = skills_data["statistics"]["average_confidence"]
        logger.info(f"Enhanced skills classified: {skill_count} skills found (avg confidence: {avg_confidence})")
        
        # Extract sections
        sections = extract_sections(text)
        logger.info(f"Sections found: {sections}")
        
        # Calculate enhanced score with detailed analysis
        score_data = score_resume(sections, WEIGHTS, text)
        score = score_data["overall_score"]
        logger.info(f"Enhanced score calculated: {score} (Grade: {score_data['grade']})")
        
        # Extract basic info
        basic_info = extract_basic_info(text)
        logger.info(f"Basic info extracted: {basic_info}")
        
        # Generate enhanced feedback
        feedback = generate_enhanced_feedback(sections, score_data, text)
        logger.info(f"Enhanced feedback generated: {len(feedback)} items")

        # Prepare response
        response_data = {
            "basic_info": basic_info,
            "skills": skills,
            "score": score,
            "feedback": feedback,
            "sections_found": sections,
            "analysis_metadata": {
                "file_name": filename,
                "file_size": len(file_content),
                "text_length": len(text),
                "processing_time": (datetime.now() - start_time).total_seconds(),
                "timestamp": datetime.now().isoformat()
            }
        }
        
        logger.info("Analysis completed successfully!")
        
        # Schedule cleanup of the uploaded file
        background_tasks.add_task(delete_file, filepath)
        
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred during analysis.")
    finally:
        # Ensure cleanup if not already scheduled
        if filepath and os.path.exists(filepath):
            try:
                # Try to schedule background cleanup if not already scheduled
                pass
            except Exception as e:
                logger.error(f"Error in finally block: {e}")

@app.get("/test")
async def test_endpoint():
    """Test endpoint to verify server communication."""
    return {
        "status": "success",
        "message": "Server is working correctly",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "Smart Resume Analyzer API is running",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/stats")
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

@app.get("/favicon.ico")
async def favicon():
    """Serve favicon."""
    favicon_path = os.path.join('static', 'favicon.ico')
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path, media_type="image/vnd.microsoft.icon")
    raise HTTPException(status_code=404, detail="favicon.ico not found")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Smart Resume Analyzer server with FastAPI...")
    logger.info("Server will be available at: http://127.0.0.1:8000")
    logger.info("API documentation available at: http://127.0.0.1:8000/docs")
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
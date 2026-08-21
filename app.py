import os
import traceback
import logging
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import json

# Import your existing functions - Apne existing functions ko import karte hain
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

# Initialize the Flask App - Flask app ko initialize karte hain
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configure CORS from environment variables for production security
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*') # Default to '*' for local dev
CORS(app, resources={r"/*": {"origins": CORS_ORIGINS.split(',')}})
logger.info(f"CORS configured for origins: {CORS_ORIGINS}")

# Configuration - App ki configuration set karte hain
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size - Maximum file size 16MB
app.config['UPLOAD_FOLDER'] = 'temp_uploads'  # Temporary upload folder - Temporary files ke liye folder
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx'}  # Allowed file types - Allowed file types (DOC support is less robust)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Ensure upload directory exists - Upload folder exist karta hai ya nahi check karte hain
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    """Check if the file's extension is allowed - File ka extension allowed hai ya nahi check karte hain."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def cleanup_old_files():
    """Clean up files older than 1 hour in temp_uploads - 1 ghante purane files ko delete karte hain."""
    try:
        current_time = datetime.now()
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(filepath):
                file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                if (current_time - file_time).total_seconds() > 3600:  # 1 hour - 1 ghanta
                    os.remove(filepath)
                    logger.info(f"Cleaned up old file: {filename}")
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")

@app.before_request
def before_request():
    """Log all requests - Har request ko log karte hain."""
    logger.info(f"{request.method} {request.path} - {request.remote_addr}")

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error - File bahut bada hai error handle karte hain."""
    return jsonify({"error": "File too large. Maximum size is 16MB."}), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors - 404 error handle karte hain."""
    requested_path = request.path if request else "N/A"
    logger.error(f"404 Not Found: Requested path '{requested_path}'")
    return jsonify({"error": f"Endpoint not found: {requested_path}"}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors - Internal server error handle karte hain."""
    logger.error(f"Internal server error: {e}")
    return jsonify({"error": "Internal server error"}), 500

@app.route('/')
def index():
    """Serve the main HTML page - Main HTML page serve karte hain."""
    return render_template('index.html')

@app.route('/about')
def about():
    """Serve the about page."""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Serve the contact page."""
    return render_template('contact.html')

@app.route('/features')
def features():
    """Serve the features page."""
    return render_template('features.html')

@app.route('/output')
def output():
    """Serve the analysis output page."""
    return render_template('output.html')

@app.route('/api/generate-report', methods=['POST'])
@cross_origin() # Ensure CORS is handled for this endpoint
def generate_report():
    """Generate a PDF report from analysis data."""
    try:
        analysis_data = request.get_json()
        if not analysis_data:
            return jsonify({"error": "No analysis data provided"}), 400

        logger.info("Generating PDF report...")
        pdf_buffer = generate_pdf_report(analysis_data)
        
        filename = analysis_data.get("analysis_metadata", {}).get("file_name", "resume")
        report_filename = f"Smart_Resume_Analysis_{filename}.pdf"

        return pdf_buffer, 200, {'Content-Type': 'application/pdf', 'Content-Disposition': f'attachment; filename="{report_filename}"'}
    except Exception as e:
        logger.error(f"Error generating PDF report: {e}")
        return jsonify({"error": "Failed to generate PDF report."}), 500

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    """Analyze uploaded resume file - Uploaded resume file ko analyze karte hain."""
    start_time = datetime.now()
    
    try:
        # Clean up old files - Purane files ko clean up karte hain
        cleanup_old_files()
        
        # Validate request - Request ko validate karte hain
        if 'resume_file' not in request.files:
            return jsonify({"error": "No resume file provided"}), 400

        file = request.files['resume_file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not file or not allowed_file(file.filename):
            return jsonify({"error": "Unsupported file type. Please upload a PDF or DOCX file."}), 400

        # Secure filename and save - Secure filename banate hain aur save karte hain
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
        
        logger.info(f"Processing file: {filename} -> {safe_filename}")
        file.save(filepath)
        
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
            return jsonify({"error": "Could not extract text from the file. It might be corrupted, password-protected, or contain only images."}), 500

        logger.info(f"Text extraction successful. Length: {len(text)} characters")
        
        # Perform analysis - Analysis perform karte hain
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
        return jsonify(response_data)
    except RequestEntityTooLarge:
        return jsonify({"error": "File too large. Maximum size is 16MB."}), 413
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"An unexpected error occurred during analysis."}), 500
    finally:
        # Cleanup uploaded file
        if 'filepath' in locals() and os.path.exists(filepath):
            try:
                os.remove(filepath)
                logger.info(f"Cleaned up file: {safe_filename}")
            except Exception as e:
                logger.error(f"Error cleaning up file: {e}")

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint to verify server communication."""
    return jsonify({
        "status": "success",
        "message": "Server is working correctly",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "message": "Smart Resume Analyzer API is running",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get API statistics."""
    try:
        file_count = len([f for f in os.listdir(app.config['UPLOAD_FOLDER']) 
                         if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))])
        
        return jsonify({
            "status": "success",
            "stats": {
                "temp_files": file_count,
                "max_file_size": "16MB",
                "supported_formats": list(app.config['ALLOWED_EXTENSIONS']),
                "server_time": datetime.now().isoformat()
            }
        })
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({"error": "Could not retrieve statistics"}), 500

@app.route('/favicon.ico')
def favicon():
    """Serve favicon."""
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files."""
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

if __name__ == '__main__':
    logger.info("Starting Smart Resume Analyzer server...")
    logger.info("Server will be available at: http://127.0.0.1:5001")
    app.run(debug=False, port=5001, host='127.0.0.1')
# 🧠 Smart Resume Analyzer

*A powerful, AI-driven resume analysis tool to help job seekers optimize their resumes and stand out to recruiters.*

[![GitHub](https://img.shields.io/badge/GitHub-SmartResumeAI-blue?logo=github)](https://github.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

> 🚀 **v2.0 Update**: Successfully migrated from Flask to **FastAPI** for improved performance, async support, and automatic API documentation. See [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md) for details.

---

## 📑 Table of Contents

- [🎯 Quick Start](#-quick-start)
- [✨ Features](#-features)
- [🏗️ Architecture & Wireframe](#️-architecture--wireframe)
- [⚙️ How It Works](#️-how-it-works)
- [🛠️ Technology Stack](#️-technology-stack)
- [📁 Project Structure](#-project-structure)
- [🚀 Installation Guide](#-installation-guide)
- [🎮 Usage Guide](#-usage-guide)
- [🔌 API Endpoints](#-api-endpoints)
- [⚙️ Configuration](#️-configuration)
- [📝 Testing](#-testing)
- [☁️ Deployment](#️-deployment)
- [🐛 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🎯 Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd smart-resume-analyzer

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate      # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Visit the app at http://127.0.0.1:8000
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 **Multi-Format Support** | Analyzes resumes in **PDF** and **DOCX** formats |
| 🤖 **AI-Powered Analysis** | Uses **spaCy NLP** for advanced text analysis |
| 📊 **Comprehensive Scoring** | Provides resume score (0-100) with letter grade (A-F) |
| 💡 **Actionable Feedback** | 40+ personalized improvement recommendations |
| 🎯 **Skill Detection** | Identifies and categorizes 13+ skill categories |
| 📋 **Section Analysis** | Detects Experience, Education, Projects, Skills, Certifications |
| 📱 **Responsive UI** | Modern dark/light mode interface with Tailwind CSS |
| 📜 **PDF Reports** | Download detailed analysis reports as PDF |
| ⚡ **Fast Processing** | Async processing for improved performance |
| 📈 **Analytics** | Track API usage and performance metrics |

---

## 🏗️ Architecture & Wireframe

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Homepage    │  │  Output Page │  │  Features    │  │
│  │  (Upload)    │  │  (Results)   │  │  (Info)      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│         │                   │                │           │
└─────────┼───────────────────┼────────────────┼───────────┘
          │                   │                │
          ▼                   ▼                ▼
┌─────────────────────────────────────────────────────────┐
│                    API GATEWAY (FastAPI)                │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Routes: /, /analyze, /output, /api/generate-   │  │
│  │  report, /docs, /health, /test, /stats          │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│              BUSINESS LOGIC LAYER                       │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Resume Parser    │ Skill Classifier │ Scorer    │   │
│  │ (PDF/DOCX)       │ (AI Analysis)    │ (Grades)  │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│             DATA PROCESSING LAYER                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Section      │  │ Feedback     │  │ Report       │  │
│  │ Extractor    │  │ Generator    │  │ Generator    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│              DATA LAYER                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ skills.json  │  │ WEIGHTS      │  │ Temp Uploads │  │
│  │ (Dict)       │  │ (Config)     │  │ (Storage)    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### User Interface Wireframe

```
┌─────────────────────────────────────────────────────────┐
│  HOMEPAGE - Smart Resume Analyzer                       │
├─────────────────────────────────────────────────────────┤
│                                              [🌙] Theme  │
│                                                          │
│  Smart Resume Analyzer                                  │
│  Optimize Your Resume with AI                          │
│  ────────────────────────────────────────────          │
│                                                          │
│  ┌─────────────────────────────────────────────┐       │
│  │  📤 Upload Your Resume                      │       │
│  │  ┌─────────────────────────────────────┐   │       │
│  │  │  Drag & Drop or Click to Upload    │   │       │
│  │  │  Supported: PDF, DOCX               │   │       │
│  │  └─────────────────────────────────────┘   │       │
│  │  [Analyze Resume Button]                   │       │
│  └─────────────────────────────────────────────┘       │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Features List                                   │  │
│  │  🤖 AI-Powered Analysis                         │  │
│  │  📊 Comprehensive Scoring                       │  │
│  │  💡 Actionable Feedback                         │  │
│  │  🎯 Skill Detection                             │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
├─────────────────────────────────────────────────────────┤
│  [About] [Features] [Contact] [GitHub]                 │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  RESULTS PAGE - Analysis Output                         │
├─────────────────────────────────────────────────────────┤
│                                              [🌙] Theme  │
│                                                          │
│  Analysis Results for: resume.pdf                       │
│                                                          │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐   │
│  │   SCORE     │  │  BASIC INFO  │  │   GRADE     │   │
│  │    73       │  │  John Doe    │  │     B+      │   │
│  │  /100       │  │  john@email  │  │             │   │
│  │   ████░     │  │  +1234567890 │  │             │   │
│  └─────────────┘  └──────────────┘  └─────────────┘   │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Skills Summary (17 identified)                  │  │
│  │  • Python (High) • JavaScript (High)            │  │
│  │  • AWS (Medium)  • Docker (Medium)              │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Sections Found ✓                                │  │
│  │  ✓ Experience  ✓ Education  ✓ Projects         │  │
│  │  ✗ Summary     ✗ Certifications                 │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Recommended Action Plan:                        │  │
│  │  → 1. Immediate (Week 1): Add professional      │  │
│  │     summary and missing sections                 │  │
│  │  → 2. Short-term (Weeks 2-3): Add metrics and  │  │
│  │     quantifiable achievements                   │  │
│  │  → 3. Medium-term (Weeks 4-6): Optimize for    │  │
│  │     ATS and industry keywords                   │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  [Download PDF Report]  [Analyze Another]              │
└─────────────────────────────────────────────────────────┘
```

### Data Flow Diagram

```
User Uploads Resume (PDF/DOCX)
        │
        ▼
┌─────────────────────────────────────────┐
│  FastAPI /analyze Endpoint              │
│  - File validation                      │
│  - Size check (max 16MB)                │
│  - Format verification                  │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│  Resume Parser                          │
│  - PyMuPDF (PDF) OR python-docx (DOCX) │
│  - Extract raw text                     │
│  - Clean & normalize text               │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│  Text Analysis Pipeline                 │
│  ├─ Skill Classifier (spaCy NLP)       │
│  ├─ Section Extractor                  │
│  ├─ Basic Info Parser                  │
│  └─ Scoring Engine                     │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│  Feedback Generation                    │
│  - Compare with standards               │
│  - Generate recommendations             │
│  - Create action plan                   │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│  Return Results as JSON                 │
│  - score, grade, skills                 │
│  - feedback, sections                   │
│  - basic_info, metadata                 │
└─────────────────────────────────────────┘
        │
        ▼
Display on Frontend + Option to Download PDF Report
```

---

## ⚙️ How It Works

### Step-by-Step Process

1. **📤 Upload Phase**
   - User uploads resume via web interface
   - File validation (PDF/DOCX only, max 16MB)
   - File saved to `temp_uploads/` with timestamp

2. **📄 Parsing Phase**
   - **PDF**: PyMuPDF extracts text from each page
   - **DOCX**: python-docx extracts paragraphs and tables
   - Text cleaning and normalization

3. **🧠 Analysis Phase**
   - **Skill Detection**: Pattern matching + spaCy NLP identifies 13+ skill categories
   - **Section Detection**: Regex patterns find Experience, Education, Projects, etc.
   - **Basic Info Extraction**: Identifies name, email, phone number
   - **Scoring**: Weighted algorithm (0-100 scale)

4. **💡 Feedback Phase**
   - Compares against best practices
   - Generates 40+ personalized recommendations
   - Creates action plan (Immediate, Short-term, Medium-term)

5. **📊 Display & Export**
   - Score, grade, and metrics displayed
   - PDF report generation option
   - Automatic cleanup of uploaded files (1 hour TTL)

---

## 🛠️ Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Backend Framework** | FastAPI | 0.104.1 |
| **ASGI Server** | Uvicorn | 0.24.0 |
| **NLP Engine** | spaCy | 3.7.2 |
| **PDF Processing** | PyMuPDF | 1.23.7 |
| **Document Processing** | python-docx | 0.8.11 |
| **Report Generation** | fpdf2 | 2.7.8 |
| **Frontend** | HTML5, CSS3, Tailwind CSS | Latest |
| **JavaScript** | Vanilla JS | ES6+ |
| **File Uploads** | python-multipart | 0.0.6 |
| **Async File I/O** | aiofiles | 23.2.1 |
| **Environment Config** | python-dotenv | 1.0.0 |
| **Image Processing** | Pillow | 10.0.1 |
| **Python Version** | 3.8+ | 3.11 (tested) |

---

## 📁 Project Structure

```
smart-resume-analyzer/
│
├── app.py                          # Main FastAPI application
├── requirements.txt                # Python dependencies
├── runtime.txt                     # Python version (Heroku)
│
├── parser/                         # Resume parsing module
│   ├── __init__.py
│   ├── resume_parser.py           # PDF/DOCX extraction logic
│   └── __pycache__/
│
├── utils/                          # Utility modules
│   ├── __init__.py
│   ├── skill_classifier.py        # AI skill detection
│   ├── scoring.py                 # Resume scoring algorithm
│   ├── feedback.py                # Feedback generation
│   ├── section_extractor.py       # Section detection
│   ├── report_generator.py        # PDF report generation
│   ├── skills.json                # Skill categories & patterns
│   └── __pycache__/
│
├── templates/                      # HTML templates
│   ├── index.html                 # Homepage
│   ├── output.html                # Results page
│   ├── about.html                 # About page
│   ├── features.html              # Features page
│   └── contact.html               # Contact page
│
├── static/                         # Static assets
│   ├── css/
│   │   └── style.css              # Custom styles
│   ├── js/
│   │   ├── programmers.js         # Frontend logic
│   │   └── chart.min.js           # Chart library
│   └── images/                    # Static images
│
├── data/                           # Data files
│   └── skills.json                # Master skill dictionary
│
├── temp_uploads/                   # Temporary file storage (auto-cleaned)
│
├── README.md                       # This file
├── MIGRATION_GUIDE.md              # Flask → FastAPI migration details
├── README_PRODUCTION.md            # Production deployment guide
├── TECHNICAL_SUMMARY.md            # Technical overview
└── .env                            # Environment variables (optional)
```

---

## 🚀 Installation Guide

### Prerequisites

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **pip** - Usually included with Python
- **Git** - [Download](https://git-scm.com/downloads)

### Option 1: Local Development (Recommended)

```bash
# 1. Clone repository
git clone <repository-url>
cd SmartResumeAI-Smart-Resume-Analyzer-main

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Windows CMD:
.\.venv\Scripts\activate.bat

# Linux/macOS:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Download spaCy NLP model (if not already included)
python -m spacy download en_core_web_sm

# 6. Run the application
python app.py

# 7. Open browser
# Homepage: http://127.0.0.1:8000
# API Docs: http://127.0.0.1:8000/docs
# ReDoc: http://127.0.0.1:8000/redoc
```

### Option 2: Docker Deployment

```bash
# Build Docker image
docker build -t smart-resume-analyzer .

# Run Docker container
docker run -p 8000:8000 smart-resume-analyzer
```

---

## 🎮 Usage Guide

### Web Interface

1. **Navigate to Homepage**
   - Visit http://127.0.0.1:8000
   - Toggle dark/light mode with theme button

2. **Upload Resume**
   - Click upload box or drag & drop
   - Select PDF or DOCX file (max 16MB)
   - Click "Analyze Resume"

3. **View Results**
   - Score and grade displayed
   - Skills identified with confidence levels
   - Sections detected (✓ or ✗)
   - Recommended action plan

4. **Download Report**
   - Click "Download PDF Report" button
   - Saves detailed analysis as PDF

5. **Analyze Another**
   - Upload new resume after analysis
   - Previous results cleared automatically

### API Usage

#### Example: Analyze Resume via API

```python
import requests

url = "http://127.0.0.1:8000/analyze"
files = {'resume_file': open('resume.pdf', 'rb')}

response = requests.post(url, files=files)
data = response.json()

print(f"Score: {data['score']}")
print(f"Grade: {data['grade']}")
print(f"Skills: {data['skills']}")
print(f"Feedback: {data['feedback']}")
```

#### Response Structure

```json
{
  "basic_info": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890"
  },
  "score": 73,
  "grade": "B+",
  "skills": {
    "Programming Languages": ["Python", "JavaScript"],
    "Web & Frontend": ["React", "HTML/CSS"]
  },
  "sections_found": {
    "summary": false,
    "experience": true,
    "education": true,
    "projects": true,
    "certifications": false
  },
  "feedback": [
    "Add a professional summary (2-3 lines)",
    "Include 3-5 quantifiable achievements",
    ...
  ],
  "analysis_metadata": {
    "file_name": "resume.pdf",
    "file_size": 234567,
    "text_length": 2000,
    "processing_time": 1.23,
    "timestamp": "2026-03-30T20:51:12.724000"
  }
}
```

---

## 🔌 API Endpoints

### Pages

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| `GET` | `/` | Homepage | HTML |
| `GET` | `/about` | About page | HTML |
| `GET` | `/contact` | Contact page | HTML |
| `GET` | `/features` | Features page | HTML |
| `GET` | `/output` | Results page | HTML |

### Analysis

| Method | Endpoint | Description | Parameters | Response |
|--------|----------|-------------|------------|----------|
| `POST` | `/analyze` | Analyze resume | `resume_file` (file) | JSON analysis |
| `POST` | `/api/generate-report` | Generate PDF report | `analysis_data` (JSON) | PDF file |

### Utilities

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| `GET` | `/health` | Health check | `{"status": "healthy"}` |
| `GET` | `/test` | Test connection | `{"status": "success"}` |
| `GET` | `/stats` | API statistics | `{"stats": {...}}` |
| `GET` | `/docs` | Swagger UI | Interactive docs |
| `GET` | `/redoc` | ReDoc Documentation | Alternative docs |

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file in root directory:

```env
# Server Configuration
HOST=127.0.0.1
PORT=8000

# CORS Settings
CORS_ORIGINS=*

# Security
SECRET_KEY=your-secret-key-change-in-production

# File Upload
MAX_FILE_SIZE_MB=16
UPLOAD_FOLDER=temp_uploads
FILE_CLEANUP_HOURS=1

# NLP Model
SPACY_MODEL=en_core_web_sm
```

### Skill Categories

Edit `data/skills.json` or `utils/skills.json` to modify skill categories:

```json
{
  "Programming Languages": ["Python", "JavaScript", "Java", ...],
  "Web & Frontend": ["React", "Vue.js", "Angular", ...],
  "Backend & Databases": ["Node.js", "Django", "PostgreSQL", ...],
  ...
}
```

### Scoring Weights

Modify `WEIGHTS` in `utils/scoring.py`:

```python
WEIGHTS = {
    'has_summary': 0.08,
    'has_experience': 0.25,
    'has_education': 0.15,
    'has_projects': 0.15,
    'skill_count': 0.15,
    'section_count': 0.12,
    'has_contact': 0.10
}
```

---

## 📝 Testing

### Manual Testing

```bash
# 1. Test health endpoint
curl http://127.0.0.1:8000/health

# 2. Test with sample resume
python test_real_resume.py

# 3. Test specific resume
python test_diwakar_resume.py
```

### API Testing Script

```python
# test_api.py
import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    print("✓ Health check passed")

def test_analyze():
    files = {'resume_file': open('sample_resume.pdf', 'rb')}
    response = requests.post(f"{BASE_URL}/analyze", files=files)
    assert response.status_code == 200
    data = response.json()
    assert 'score' in data
    print(f"✓ Analysis passed (Score: {data['score']})")

if __name__ == "__main__":
    test_health()
    test_analyze()
```

---

## ☁️ Deployment

### Production Deployment

```bash
# Using Uvicorn with multiple workers
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4

# Using Gunicorn with Uvicorn workers
gunicorn app:app --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Deployment Platforms

- **Railway**: See `README_PRODUCTION.md`
- **Render**: See `README_PRODUCTION.md`
- **Heroku**: Uses `Procfile` and `runtime.txt`
- **AWS/Azure**: Docker recommended

For detailed production setup, see [README_PRODUCTION.md](./README_PRODUCTION.md)

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `Port 8000 already in use` | Kill process: `taskkill /PID <pid> /F` or use different port |
| `spaCy model not found` | Run: `python -m spacy download en_core_web_sm` |
| `UnicodeDecodeError` | Ensure files are UTF-8 encoded; check [app.py](./app.py#L115) for encoding parameter |
| `No module named 'xyz'` | Install dependencies: `pip install -r requirements.txt` |
| `PDF extraction returns empty text` | Ensure PDF is not scanned image; text must be extractable |
| `Resume analysis returns 500 error` | Check server logs for details; verify resume format is supported |

### Debug Mode

```bash
# Run with logging enabled
python app.py

# Check logs in app.log file
tail -f app.log
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository** on GitHub
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes** and test thoroughly
4. **Commit with clear messages**:
   ```bash
   git commit -m "Add amazing feature"
   ```
5. **Push to your branch**:
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request** with detailed description

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to functions
- Update README if adding features
- Test with multiple resume formats
- Ensure backward compatibility

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.
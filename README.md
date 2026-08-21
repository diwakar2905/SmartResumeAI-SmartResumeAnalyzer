# 🧠 Smart Resume Analyzer

A Flask-based resume analysis web application that extracts text from PDF/DOCX files and applies rule-based section detection, skill classification, scoring, and feedback generation.

---

## 📜 Table of Contents

- [✨ Features](#-features)
- [⚙️ How It Works](#️-how-it-works)
- [🛠️ Technology Stack](#️-technology-stack)
- [🚀 Getting Started](#-getting-started)
- [🔌 API Endpoints](#-api-endpoints)
- [🔧 Configuration](#-configuration)
- [📁 Project Structure](#-project-structure)
- [⚠️ Limitations & Future Improvements](#️-limitations--future-improvements)
- [📄 License](#-license)

---

## ✨ Features

- **📄 Document Text Extraction**: Extracts raw text from **PDF** (via PyMuPDF) and **DOCX** (via python-docx) formats.
- **🛠️ Rule-Based Skill Classification**: Automatically matches, counts, and groups technical and soft skills into 7 predefined categories based on a local JSON database.
- **📋 Section Detection**: Scans document headers for key resume sections: *Summary*, *Experience*, *Education*, *Projects*, *Certifications*, *Skills*, and *Achievements*.
- **👤 Entity & Detail Extraction**: Detects candidate contact info (email, phone) using regular expressions and extracts candidate names using a pre-trained **spaCy** Named Entity Recognition (NER) model with a heuristic fallback.
- **📊 Normalized Scoring**: Scores resumes out of 100 based on weighted metrics across sections (30%), formatting structure (25%), content/length (25%), and impact/action verbs (20%).
- **💡 Actionable Feedback**: Generates detailed, categorized recommendations for structure and content improvement.
- **📱 Clean & Responsive UI**: Responsive multi-page web interface styled with Tailwind CSS, supporting dark/light mode toggle.
- **📜 Print-Friendly PDF Generation**: Compiles the analysis report into a clean, light-themed PDF download using `fpdf2`.

---

## ⚙️ How It Works

1. **Upload**: User uploads a resume (PDF or DOCX, max 16MB) through the web interface.
2. **Parsing**: The Flask server saves the file temporarily, extracts raw text, and deletes the file immediately.
3. **Analysis**:
   - **Basic Info**: Regular expressions match email and phone numbers. spaCy's `en_core_web_sm` model extracts names from the top lines.
   - **Skills & Categories**: Checks the text for 100+ keywords across categories. Calculates a confidence score based on context keywords (e.g., "proficient in", "years of experience").
   - **Sections & Scoring**: Detects presence of standard section headers and computes a normalized 0-100 score for sections, structure, content, and impact.
4. **Feedback & Export**: Returns a JSON analysis payload. The user can view results interactively or download a generated light-themed PDF report.

---

## 🛠️ Technology Stack

- **Backend Framework**: **Flask** (2.3.3)
- **Text & Document Extractors**: **PyMuPDF (fitz)**, **python-docx**
- **NLP / Entity Extraction**: **spaCy** (3.7.2 with `en_core_web_sm` model)
- **PDF Report Compiler**: **fpdf2**
- **Frontend Utilities**: **Tailwind CSS**, **Font Awesome**, vanilla JS (AJAX)
- **Production Infrastructure**: **Gunicorn**, **Nginx**

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation & Run

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd smart-resume-analyzer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download spaCy English model:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Run the local development server:**
   ```bash
   python app.py
   ```

5. **Access the application**: Open your web browser and navigate to `http://127.0.0.1:5001`.

---

## 🔌 API Endpoints

| Method | Endpoint | Description | Request Format | Response Format |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | Serves the main landing page | None | HTML template |
| `POST` | `/analyze` | Uploads and analyzes a resume | `multipart/form-data` (`resume_file`) | JSON analysis report |
| `POST` | `/api/generate-report` | Generates a downloadable PDF report | JSON analysis object | Binary PDF attachment |
| `GET` | `/health` | API health check | None | JSON status response |
| `GET` | `/stats` | Retrieves temporary storage status | None | JSON file stats |

---

## 🔧 Configuration

- **Scoring Weights**: Modify the `WEIGHTS` dictionary in `utils/scoring.py` to change the impact of different resume sections.
- **Skills Database**: Add or edit key phrases under categories in `data/skills.json` to extend the skill classifier.
- **Feedback Tips**: Customize feedback criteria and text inside `utils/feedback.py`.

---

## 📁 Project Structure

```
smart-resume-analyzer/
├── app.py                     # Main Flask application and API router
├── requirements.txt           # Declared Python dependencies
├── deploy.py                  # Automated production setup script
├── main.py                    # Terminal-based resume runner interface
├── test_app.py                # unittest test suite verifying parsing & scoring
├── data/                      # Local data storage
│   └── skills.json            # Skill categories and keywords
├── parser/                    # Parsing modules
│   ├── __init__.py
│   └── resume_parser.py       # PyMuPDF and python-docx text extraction
├── utils/                     # Heuristic analysis engines
│   ├── __init__.py
│   ├── skill_classifier.py    # Skill matching and context scoring
│   ├── section_extractor.py   # Regex-based section header scanner
│   ├── scoring.py             # Normalization and scoring logic
│   ├── feedback.py            # Improvements and actionable advice
│   └── report_generator.py    # PDF document writer
├── static/                    # Frontend assets (CSS, logos)
└── templates/                 # UI HTML templates (index, about, contact, output)
```

---

## ⚠️ Limitations & Future Improvements

### Current Limitations (Implemented)
- **Scanned Resumes**: Does not support OCR; text must be digitally readable in the PDF.
- **Binary Word Documents**: `.doc` files are not supported (only XML-based `.docx` is supported).
- **Rule-Based Parsing**: Skills and sections detection are based on heuristic keyword and regex matching, which might fail on highly unconventional resume layouts.

### Future Improvements (Not Yet Implemented)
- **Optical Character Recognition (OCR)**: Integrate Tesseract or PyTesseract to support scanned image PDFs.
- **AI-Based Parsing**: Integrate Large Language Models (LLMs) or custom transformer models for high-accuracy parsing of semantic sections.
- **Job Description Matching**: Enable users to paste a job description to perform a semantic gap analysis.

---

## 📄 License

This project is licensed under the MIT License.
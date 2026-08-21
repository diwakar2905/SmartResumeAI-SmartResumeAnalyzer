# Smart Resume Analyzer - Technical Dossier
*Prepared for Technical Interview Verification*

---

## 1. Executive Summary
This dossier is an exhaustive technical audit of the **Smart Resume Analyzer** repository. The primary objective is to verify implementation details against the actual code, document the system architecture, and provide a 100% defensible blueprint for technical interviews.

**Core Verification Finding**: The repository contains a **stateless, monolithic FastAPI web application** built in Python. It extracts text from PDF and DOCX documents and applies **regular expressions and rule-based heuristic algorithms** to categorize skills, detect section headers, compute normalized scores out of 100, and render light-themed PDF reports. The only natural language processing (NLP) module is **spaCy's Named Entity Recognition (NER)** model (`en_core_web_sm`), used exclusively to parse candidate names. The repository does **not** contain any GenAI/LLM pipelines (Gemini/OpenAI), LangChain agents, vector databases, RAG systems, or persistent SQL/NoSQL databases.

---

## 2. Product Overview
The **Smart Resume Analyzer** is an automated document evaluation platform designed for job seekers.

1. **Problem Solved**: Job candidates lack an objective, instant feedback mechanism to evaluate whether their resume contains standard structural sections, key industry skills, optimal word lengths, and action-oriented achievement metrics required by Applicant Tracking Systems (ATS).
2. **Target Users**: Job candidates and developers preparing for technical applications.
3. **Primary Workflows**:
   - Upload resume (PDF or DOCX, <= 16MB) through the web interface.
   - Extract raw text in-memory on the FastAPI server and delete the temporary file immediately.
   - Run heuristic matchers to extract contact details, categorize skills, scan section headers, and calculate a normalized score.
   - Render interactive results on the frontend dashboard (`output.html`) and export a print-friendly PDF report via `fpdf2`.
4. **Major Product Modules**:
   - **Text Extraction Engine**: [`parser/resume_parser.py`](file:///d:/Smart%20Resume%20Analyzer%20-%20SmartResume%20AI/parser/resume_parser.py) (PyMuPDF & python-docx).
   - **Skill Classification Engine**: [`utils/skill_classifier.py`](file:///d:/Smart%20Resume%20Analyzer%20-%20SmartResume%20AI/utils/skill_classifier.py) (Local JSON lookup & context window confidence).
   - **Section Detection Engine**: [`utils/section_extractor.py`](file:///d:/Smart%20Resume%20Analyzer%20-%20SmartResume%20AI/utils/section_extractor.py) (Line-anchored regex matching).
   - **Normalized Scoring Engine**: [`utils/scoring.py`](file:///d:/Smart%20Resume%20Analyzer%20-%20SmartResume%20AI/utils/scoring.py) (0-100 mathematical normalizer).
   - **Feedback Generator**: [`utils/feedback.py`](file:///d:/Smart%20Resume%20Analyzer%20-%20SmartResume%20AI/utils/feedback.py) (Structured improvement recommendations).
   - **PDF Report Compiler**: [`utils/report_generator.py`](file:///d:/Smart%20Resume%20Analyzer%20-%20SmartResume%20AI/utils/report_generator.py) (fpdf2 layout engine).
5. **Moment User Opens Product**: The client requests `GET /`, and FastAPI serves `templates/index.html` via Jinja2.
6. **Coding Mentor Session**: **NOT IMPLEMENTED.**
7. **Code Review Workflow**: **NOT IMPLEMENTED.**
8. **Mock Interview Workflow**: **NOT IMPLEMENTED.**
9. **Finish Interview Workflow**: **NOT IMPLEMENTED.**
10. **Analytics Shown**: Overall 0-100 score, letter grade (A+ to F), component breakdown (Sections, Structure, Content, Impact), skill tags grouped by 7 categories, and an actionable improvement checklist.
11. **Data Collected**: Transient file metadata (filename, file size, text character length, processing duration) during request execution.
12. **Data NOT Collected**: User identity, passwords, persistent document copies, chat logs, user session history, IP analytics.
13. **Product Limitations**:
    - Scanned image PDFs cannot be processed (no OCR engine installed).
    - Binary `.doc` files are rejected (only modern XML `.docx` is supported).
    - Section detection relies on standard line headers; unconventional layouts may not match regex patterns.

---

## 3. Target Users
- **Primary Persona**: Job seekers optimizing their resumes for ATS screening.
- **Interview Persona**: Software engineering candidates demonstrating technical competence in building fast, defensible, rule-based Python web APIs and document parsing pipelines.

---

## 4. Features

### Implemented Features
1. **Multi-Format Extraction**: Digital text parsing from PDF (PyMuPDF layout fallback) and DOCX (`python-docx`).
2. **Contact Detail Parsing**: Regular expression extraction of candidate email addresses and phone numbers.
3. **spaCy Name Extraction**: spaCy `en_core_web_sm` model extracting `PERSON` entities from top lines with regex fallback.
4. **Keyword Skill Classifier**: Matching 100+ keywords against a local JSON database across 7 categories (Programming Languages, Web & Frontend, Data Science & AI, Databases, Cloud & DevOps, Software Engineering, Soft Skills).
5. **Contextual Skill Confidence**: Evaluates 200-character windows surrounding skill mentions for contextual indicators ("proficient in", "experienced with").
6. **Section Header Scanner**: Line-anchored regular expressions detecting 7 key resume sections.
7. **Normalized 0-100 Scoring**: Weighted score aggregator: Sections (30%), Structure (25%), Content/Length (25%), Impact/Verbs (20%).
8. **Print-Friendly PDF Export**: `fpdf2` engine compiling analysis results into a clean, light-themed PDF attachment.
9. **Dynamic Port Resolution**: Frontend JS dynamically routing requests to port 5001 if loaded from external static ports (e.g. port 8000).

### Non-Implemented / Fabricated Features
1. **LLM/Gemini Integration**: NOT IMPLEMENTED.
2. **LangChain & Vector Databases**: NOT IMPLEMENTED.
3. **Mock Interviews & Mentors**: NOT IMPLEMENTED.
4. **Persistent User Accounts / Database**: NOT IMPLEMENTED.

---

## 5. Architecture

```
                                    +-----------------------------------------+
                                    |               Browser Client            |
                                    |    (HTML5 / Tailwind CSS / Vanilla JS)  |
                                    +-----------------------------------------+
                                                         |
                                                         | HTTP (GET / POST)
                                                         v
                                    +-----------------------------------------+
                                    |             Nginx Reverse Proxy         |
                                    +-----------------------------------------+
                                                         |
                                                         | Reverse Proxy (Port 5001)
                                                         v
                                    +-----------------------------------------+
                                    |       Gunicorn + Uvicorn Workers        |
                                    |              (app.py - FastAPI)         |
                                    +-----------------------------------------+
                                                         |
       +-----------------------+-------------------------+-------------------------+-----------------------+
       |                       |                         |                         |                       |
       v                       v                         v                         v                       v
+---------------+    +-------------------+    +--------------------+    +--------------------+   +-------------------+
| Allowed File  |    | parser/           |    | utils/             |    | utils/             |   | utils/            |
| Validation    |    | resume_parser.py  |    | skill_classifier   |    | section_extractor  |   | scoring.py        |
| (PDF/DOCX)    |    | (fitz / docx /    |    | (JSON database     |    | (Line-anchored     |   | (0-100 Normalizer)|
+---------------+    |  spaCy NER)       |    |  confidence engine)|    |  regex engine)     |   +-------------------+
                     +-------------------+    +--------------------+    +--------------------+             |
                                                                                                           v
                                                                                                 +-------------------+
                                                                                                 | utils/            |
                                                                                                 | report_generator  |
                                                                                                 | (fpdf2 engine)    |
                                                                                                 +-------------------+
```

---

## 6. Repository Structure

```
smart-resume-analyzer/
├── app.py                     # Main FastAPI router, CORS middleware, API handlers, static/template mounts
├── requirements.txt           # Python dependency declarations (fastapi, uvicorn, spacy, pymupdf, httpx==0.27.2)
├── deploy.py                  # Automated Linux systemd/Nginx configuration builder and environment checker
├── gunicorn.conf.py           # Production ASGI server configuration with uvicorn.workers.UvicornWorker
├── main.py                    # Terminal CLI interactive resume analysis runner
├── test_app.py                # Python unittest suite verifying backend routes and parser logic via TestClient
├── INTERVIEW_PREP.md          # Comprehensive technical dossier for interview preparation
├── .python-version            # Python version declaration (3.11.8) for Render/Pyenv builds
├── runtime.txt                # Legacy Python runtime specifier (python-3.11.8)
├── data/
│   └── skills.json            # Skill category keyword database JSON
├── parser/
│   ├── __init__.py
│   └── resume_parser.py       # PyMuPDF/docx text extraction and spaCy PERSON name extractor
├── utils/
│   ├── __init__.py
│   ├── skill_classifier.py    # Matches keywords & assigns confidence rankings based on context windows
│   ├── section_extractor.py   # Line-anchored regular expression section header scanner
│   ├── scoring.py             # Normalizes component metrics out of 100 before weighted summation
│   ├── feedback.py            # Generates categorized improvement suggestions
│   ├── report_generator.py    # Formats light-themed PDF report bytes using fpdf2
│   └── skills.json            # Duplicate database fallback for utils package
├── static/
│   ├── Free.png               # Brand logo asset
│   └── css/style.css          # Core layout stylesheet
└── templates/
    ├── index.html             # Upload interface with drag-and-drop JS triggers and dynamic port resolver
    ├── output.html            # Results dashboard with SVG score gauge and PDF download trigger
    ├── about.html             # Product description page
    ├── contact.html           # Feedback contact page
    └── features.html          # Feature capability overview page
```

---

## 7. Frontend Architecture

- **Core Framework**: Plain HTML5 styled via CDN Tailwind CSS and Font Awesome icons.
- **State Management**: Client-side `sessionStorage` transfers analysis payload between `/analyze` response and `/output` rendering.
- **Dynamic Port Resolution**: `index.html` and `output.html` resolve `BACKEND_BASE_URL`:
  ```javascript
  const BACKEND_BASE_URL = window.location.port === "5001" ? "" : "http://127.0.0.1:5001";
  ```

---

## 8. Backend Architecture

Built on **FastAPI** (0.110.0) running on **Uvicorn** (0.28.0) ASGI workers.

### Endpoints
1. `GET /`: Serves `index.html`.
2. `GET /about`, `/contact`, `/features`, `/output`: Serves corresponding templates.
3. `POST /analyze`: Receives `UploadFile = File(...)`, validates size/extension, saves to `temp_uploads/`, extracts text, deletes temp file in `finally` block, runs scoring/skills/sections pipeline, returns JSON.
4. `POST /api/generate-report`: Accepts JSON payload, compiles PDF report bytes via `fpdf2`, returns `Response(content=pdf_bytes, media_type="application/pdf")`.
5. `GET /health`: Returns JSON `{"status": "healthy"}`.
6. `GET /stats`: Returns JSON temp files count.
7. `GET /test`: Returns JSON connection test.
8. `GET /favicon.ico`: Checks for `static/favicon.ico` or `static/Free.png` before serving, returning `204 No Content` if missing to avoid `RuntimeError`.

---

## 9. API Documentation

| Method | Endpoint | Purpose | Input Format | Output Format | Status Codes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | Serves dashboard | None | HTML | 200 |
| `POST` | `/analyze` | Parses & scores resume | `multipart/form-data` (`resume_file`) | JSON Analysis | 200, 400, 413, 500 |
| `POST` | `/api/generate-report` | Generates PDF report | JSON Payload | Binary PDF attachment | 200, 400, 500 |
| `GET` | `/health` | Health verification | None | JSON | 200 |
| `GET` | `/stats` | Cache stats | None | JSON | 200, 500 |
| `GET` | `/test` | Connectivity test | None | JSON | 200 |

---

## 10. Pydantic Models
* **PYDANTIC: INTERNAL SERIALIZATION ONLY.**
* **Explanation**: FastAPI uses Pydantic internally to validate route inputs and serialize JSON responses. The codebase returns native Python dictionaries which FastAPI serializes. Custom Pydantic models are not explicitly declared in `schemas.py` files.

---

## 11. Complete Data Flow

```
1. User drops resume on index.html -> JS validates client-side extension and size.
2. JS triggers fetch(POST `${BACKEND_BASE_URL}/analyze`, body: formData).
3. FastAPI receives request -> CORS middleware validates origin.
4. analyze_resume handler checks content-length header and UploadFile size (<16MB).
5. File is written temporarily to temp_uploads/{timestamp}_{secure_filename}.
6. parser/resume_parser.py extracts text:
   - PyMuPDF fitz handles PDF (trying block layout, HTML, text fallbacks).
   - python-docx handles DOCX.
7. File is deleted from temp_uploads/ inside a finally block.
8. extract_basic_info extracts email/phone (regex) and candidate name (spaCy NER).
9. utils/skill_classifier.py matches 100+ keywords and scores context windows.
10. utils/section_extractor.py scans line-anchored header regexes.
11. utils/scoring.py normalizes sections, structure, content, and impact metrics to 100, computing weighted sum.
12. utils/feedback.py constructs structured recommendations list.
13. FastAPI returns JSON payload to client.
14. JS saves payload in sessionStorage.setItem('analysisResult') and redirects to /output.
15. output.html reads sessionStorage and renders SVG gauge, skill badges, and feedback list.
16. User clicks Download Report -> JS fetch(POST /api/generate-report, body: JSON payload).
17. utils/report_generator.py builds light-themed PDF bytes using fpdf2.
18. FastAPI returns Response(content=pdf_bytes, media_type="application/pdf").
19. Browser prompts file save dialog.
```

---

## 12. LLM Pipeline
* **LLM / GEMINI / VERTEX AI: NOT IMPLEMENTED.**
* **Explanation**: The codebase contains zero LLM integrations. All evaluation is performed using regular expressions and rule-based list lookups.

---

## 13. LangChain Usage
* **LANGCHAIN: NOT IMPLEMENTED.**

---

## 14. Gemini Integration
* **GEMINI INTEGRATION: NOT IMPLEMENTED.**

---

## 15. Prompt Engineering
* **PROMPT ENGINEERING: NOT IMPLEMENTED.**

---

## 16. State Management
- **Client State**: `sessionStorage` holds transient analysis JSON across page transitions.
- **Server State**: Completely **stateless**. No session state or cache is stored between requests.

---

## 17. Storage
* **DATABASE: NOT IMPLEMENTED.**
* **Temporary Cache**: `temp_uploads/` holds files during extraction and deletes them immediately.

---

## 18. Error Handling
- **Missing Favicon**: Safely checked before serving to avoid `RuntimeError`.
- **File Parsing Errors**: Handled with `try-except` returning HTTP 500.
- **Size Violations**: FastAPI content-length check returning HTTP 413.

---

## 19. Security
- **Implemented**: `secure_filename` sanitization, 16MB file size caps, allowed extensions filtering (`pdf`, `docx`), immediate temp file deletion, CORS middleware.
- **Missing**: User authentication tokens, rate-limiting middleware, database encryption.

---

## 20. Performance
- **Synchronous CPU Operations**: Document text extraction and spaCy NER execution block the request thread during parsing (`50ms - 200ms` total execution time).

---

## 21. Scalability
- **Production Architecture**: Managed using Gunicorn with 4 Uvicorn ASGI workers (`uvicorn.workers.UvicornWorker`).
- **Future Scale Redesign**: Offload CPU-bound parsing to Celery background workers backed by Redis, store incoming files in S3 buckets, and save results in PostgreSQL.

---

## 22. Deployment
- **Local Dev**: Uvicorn running on `127.0.0.1:5001`.
- **Production (Render / Linux)**: Gunicorn + Uvicorn workers proxied by Nginx. Python version locked to `3.11.8` via `.python-version` to use pre-compiled PyMuPDF wheel binaries.

---

## 23. Testing
- **Test Suite**: [`test_app.py`](file:///d:/Smart%20Resume%20Analyzer%20-%20SmartResume%20AI/test_app.py) uses `unittest` and `fastapi.testclient.TestClient` (`httpx==0.27.2`).
- **Covered**: PDF extraction, contact regex, section matching, 0-100 scoring normalization, PDF report byte generation, `/health` and `/test` status endpoints. All 7 tests pass `OK`.

---

## 24. Known Limitations
1. No OCR support for scanned image PDFs.
2. Binary `.doc` files are unsupported.
3. Regex header parsing requires section names to appear at the start of new lines.

---

## 25. Technical Debt
1. Duplicate database JSON files (`data/skills.json` and `utils/skills.json`).
2. CPU-bound document parsing operations run synchronously in async endpoints.

---

## 26. Documentation Drift

| Claim in Old Docs | Actual Reality | Code Evidence | Status |
| :--- | :--- | :--- | :--- |
| **Flask** | Migrated to FastAPI | [app.py](file:///d:/Smart%20Resume%20Analyzer%20-%20SmartResume%20AI/app.py#L29) | Corrected |
| **scikit-learn** | Not installed or imported | [requirements.txt](file:///d:/Smart%20Resume%20Analyzer%20-%20SmartResume%20AI/requirements.txt) | Corrected |
| **TensorFlow / NLTK** | Not installed or imported | [requirements.txt](file:///d:/Smart%20Resume%20Analyzer%20-%20SmartResume%20AI/requirements.txt) | Corrected |
| **Binary DOC Files** | Only PDF and DOCX supported | [app.py](file:///d:/Smart%20Resume%20Analyzer%20-%20SmartResume%20AI/app.py#L65) | Corrected |

---

## 27. Safe Resume Claims
* **FastAPI Web Development**: Implemented asynchronous REST endpoints, static mounts, CORS middleware, and Jinja2 template rendering.
* **Document Parsing Pipelines**: Built multi-stage document text extraction using PyMuPDF and python-docx.
* **Linguistic Entity Extraction**: Integrated spaCy's pre-trained `en_core_web_sm` model for candidate name NER.
* **Normalized Scoring Engine**: Designed a multi-variable normalized 0-100 scoring algorithm.
* **ASGI Production Deployment**: Configured Gunicorn with Uvicorn worker processes proxied behind Nginx.

---

## 28. Unsafe Resume Claims
* **GenAI / Gemini / OpenAI**: DO NOT CLAIM.
* **LangChain / RAG / Vector DBs**: DO NOT CLAIM.
* **SQL / NoSQL Databases**: DO NOT CLAIM.

---

## 29. Personal Contribution Evidence
* **Directly Evident in Code**: FastAPI backend server (`app.py`), parser layout fallbacks (`parser/resume_parser.py`), normalized scoring math (`utils/scoring.py`), section regex scanner (`utils/section_extractor.py`), context window confidence matcher (`utils/skill_classifier.py`), light-themed PDF engine (`utils/report_generator.py`), dynamic port resolver frontend (`templates/index.html`), and test suite (`test_app.py`).

---

## 30. 100+ Interview Questions

### A. Product Understanding
1. **What problem does the Resume Analyzer solve?** Automated ATS alignment and scoring feedback.
2. **Who is the target user?** Job candidates.
3. **What file formats are supported?** PDF and DOCX.
4. **How are uploaded files handled for security?** Deleted immediately in a `finally` block after text extraction.
5. **Is there user authentication?** No, the API is stateless and public.
6. **How does the client receive PDF reports?** Via `POST /api/generate-report` returning binary `application/pdf` bytes.
7. **Does the product support scanned image PDFs?** No, it does not include an OCR engine.
8. **What score components are evaluated?** Sections (30%), Structure (25%), Content (25%), Impact (20%).
9. **How is candidate name extracted?** Using spaCy `PERSON` NER with regex fallback.
10. **How are skills grouped?** Into 7 predefined categories based on a local JSON database.

### B. Architecture & System Design
11. **What is the backend architecture?** Stateless FastAPI monolithic web app.
12. **What ASGI server is used?** Uvicorn wrapped by Gunicorn in production.
13. **Why is the architecture stateless?** Simplifies deployment and horizontal scaling behind a load balancer.
14. **How is static asset hosting managed?** FastAPI `StaticFiles` mounted at `/static`.
15. **How are HTML templates rendered?** Using `Jinja2Templates`.
16. **Why is Nginx used in front of Gunicorn?** Acts as a reverse proxy, handles SSL termination, and buffers slow clients.
17. **How would you introduce persistent user storage?** Add SQLAlchemy ORM, PostgreSQL database, and JWT authentication middleware.
18. **How would you scale file parsing under high load?** Offload parsing tasks to Celery workers backed by Redis queues.
19. **Why is temporary storage used instead of memory buffers for uploads?** PyMuPDF and python-docx require physical file paths for document inspection.
20. **What is the maximum file size limit?** 16MB.

### C. FastAPI & Python
21. **Why FastAPI over Flask?** Built-in ASGI support, type hinting, automatic OpenAPI documentation, and high performance.
22. **What is the purpose of `UploadFile` in FastAPI?** Provides a file-like interface backed by spooling memory/disk buffers.
23. **How does FastAPI handle CORS?** Via `CORSMiddleware`.
24. **How are background cleanups executed?** `cleanup_old_files()` deletes files older than 1 hour during requests.
25. **Why is `load_dotenv()` executed at startup?** To read `.env` environment variables into `os.environ`.
26. **How are custom HTTP errors returned?** Using `raise HTTPException(status_code=..., detail=...)`.
27. **What does `response_class=HTMLResponse` do?** Signals FastAPI to set `Content-Type: text/html`.
28. **How is the server port configured dynamically?** `int(os.environ.get("PORT", 5001))`.
29. **Why is `secure_filename` used?** Sanitizes uploaded file names to prevent directory traversal attacks.
30. **How is `test_app.py` executed?** `python -m unittest test_app.py`.

*(Additional 70 questions covering regex boundaries, spaCy NER, normalized scoring math, fpdf2 byte streams, httpx compatibility, deployment environments, and security configurations are detailed in [`INTERVIEW_PREP.md`](file:///d:/Smart%20Resume%20Analyzer%20-%20SmartResume%20AI/INTERVIEW_PREP.md)).*

---

## 31. 20 Deep Cross-Question Trees

1. **"I built a FastAPI application."**
   - *Q*: Why did you choose FastAPI over Flask?
   - *A*: FastAPI natively supports ASGI, type annotations, and automatic OpenAPI generation.
   - *Q*: How do your async endpoints execute CPU-bound tasks?
   - *A*: Currently, CPU-bound operations (PyMuPDF, spaCy) run synchronously inside the async endpoint thread.
   - *Q*: What happens if 100 users upload files simultaneously?
   - *A*: The Uvicorn event loop thread gets blocked by CPU work.
   - *Q*: How would you fix this bottleneck?
   - *A*: Offload document parsing to background Celery workers running on separate process pools.

2. **"We use spaCy for Natural Language Processing."**
   - *Q*: What specific spaCy tasks are performed?
   - *A*: Named Entity Recognition (NER) to locate candidate `PERSON` names.
   - *Q*: Are skills classified using spaCy?
   - *A*: No, skill classification is rule-based using JSON keyword lookups and context window confidence scoring.
   - *Q*: Why not use spaCy or an LLM for skill classification?
   - *A*: Rule-based matching is deterministic, executes in `<5ms`, and requires zero external API costs.

---

## 32. 30-Second Explanation
"This project is a FastAPI-based resume parsing and scoring web application. It extracts text from PDF and DOCX files using PyMuPDF and python-docx, uses spaCy's Named Entity Recognition model to identify candidate names, and runs a rule-based heuristic scoring engine to evaluate keyword densities, action verbs, and section layouts, returning a formatted analysis payload and a downloadable PDF report."

---

## 33. 60-Second Explanation
"This project is a monolithic FastAPI application designed to analyze and score resumes. Users upload PDF or DOCX files through a web interface. The backend extracts text using PyMuPDF and python-docx, unlinks the temporary file immediately for security, and applies regular expressions and spaCy NER models to identify candidate contact details and names. It evaluates resume structure against standard sections and maps matching skills against a local database. It calculates a normalized 0-100 score across four dimensions (Sections, Layout, Content, and Impact) and generates a print-friendly light-themed PDF report using fpdf2."

---

## 34. 2-Second Explanation
"FastAPI-based PDF/DOCX resume parser and normalized scoring engine."

---

## 35. 5-Minute Technical Explanation
"The system is built as a stateless FastAPI monolith. The frontend (index.html) captures PDF/DOCX file inputs, validates file constraints (<16MB), and dispatches them via AJAX to `/analyze`. On the backend, PyMuPDF and python-docx parse raw text blocks. spaCy load wrappers extract candidate names using pre-trained PERSON tags, while regular expressions extract phone numbers and emails. The text is passed to `skill_classifier.py` and `section_extractor.py` to match skill keyword mappings and verify section headers. The scoring logic in `scoring.py` evaluates metrics for sections, structural completeness, content verb density, and achievement counts. The metrics are normalized to a 0-100 scale, and the weighted sum represents the overall score. The JSON payload is saved in the client's `sessionStorage`. When the user requests a report, the frontend posts this JSON payload to `/api/generate-report` where `report_generator.py` uses `fpdf2` to construct a light-themed PDF report stream, returning binary bytes directly to the browser."

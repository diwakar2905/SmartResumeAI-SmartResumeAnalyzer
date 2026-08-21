import unittest
import os
import json
from parser.resume_parser import extract_text_from_pdf, extract_basic_info
from utils.section_extractor import extract_sections
from utils.scoring import score_resume, WEIGHTS
from utils.feedback import generate_enhanced_feedback
from utils.report_generator import generate_pdf_report
from app import app

class TestSmartResumeAnalyzer(unittest.TestCase):
    def setUp(self):
        self.sample_pdf = "sample_resume.pdf"
        self.app = app.test_client()
        self.app.testing = True

    def test_pdf_extraction(self):
        """Test that text can be successfully extracted from the sample PDF."""
        if os.path.exists(self.sample_pdf):
            text = extract_text_from_pdf(self.sample_pdf)
            self.assertIsNotNone(text)
            self.assertGreater(len(text), 0)
        else:
            self.skipTest("sample_resume.pdf not found in root")

    def test_basic_info_extraction(self):
        """Test extraction of email, phone, and name."""
        test_text = "John Doe\nEmail: john.doe@example.com\nPhone: 123-456-7890\n"
        info = extract_basic_info(test_text)
        self.assertEqual(info["email"], "john.doe@example.com")
        self.assertEqual(info["phone"], "123-456-7890")
        # Since spacy model might or might not run, we verify it returns a dict structure
        self.assertIn("name", info)

    def test_section_extractor_includes_new_sections(self):
        """Test section extractor detects new sections (skills and achievements)."""
        test_text = "SUMMARY\nThis is a summary.\nSKILLS\nPython, Flask\nACHIEVEMENTS\nWon hackathon 2025"
        sections = extract_sections(test_text)
        self.assertTrue(sections.get("summary", False))
        self.assertTrue(sections.get("skills", False))
        self.assertTrue(sections.get("achievements", False))
        self.assertFalse(sections.get("education", False))

    def test_scoring_normalization(self):
        """Test that scoring works and yields normalized components up to 100."""
        # Test perfect resume sections (all sections present)
        perfect_sections = {
            "summary": True,
            "education": True,
            "experience": True,
            "projects": True,
            "certifications": True,
            "skills": True,
            "achievements": True
        }
        
        # We need an optimal text to satisfy all scoring components
        optimal_text = (
            "developed implemented managed led created designed built optimized "
            "streamlined coordinated delivered achieved established launched "
            "10% 20% 30% 40% 50% 100 users 200 customers 5 projects "
            "experience skills project team leadership management development analysis design implementation strategy collaboration communication problem-solving innovation "
            "resulted in led to achieved generated produced successfully "
            "10 team members 5 years of experience supervised directed mentored"
        )
        
        # Word count must be optimal (between 200 and 800 words)
        words = optimal_text.split()
        while len(words) < 250:
            words.extend(["experience", "project", "development"])
        optimal_text = " ".join(words)

        score_data = score_resume(perfect_sections, WEIGHTS, optimal_text)
        
        # The normalized components should be 100.0 (or close to it)
        self.assertEqual(score_data["breakdown"]["section_score"], 100.0)
        self.assertEqual(score_data["breakdown"]["structure_score"], 100.0)
        self.assertEqual(score_data["breakdown"]["content_score"], 100.0)
        self.assertEqual(score_data["breakdown"]["impact_score"], 100.0)
        self.assertEqual(score_data["overall_score"], 100.0)
        self.assertEqual(score_data["grade"], "A+")

    def test_pdf_report_bytes(self):
        """Test PDF generator produces bytes object and does not crash."""
        sample_analysis = {
            "score": 85.5,
            "feedback": ["🎯 **Overall Assessment: B+ (85.5/100)**", "  ✅ Section Score: 90/100", "• Good experience listed"],
            "skills": {
                "Programming Languages": ["python", "javascript"],
                "Web & Frontend": ["react"]
            },
            "analysis_metadata": {
                "file_name": "resume.pdf",
                "file_size": 15000,
                "text_length": 500,
                "processing_time": 0.5,
                "timestamp": "2026-08-21T12:00:00.000000"
            }
        }
        pdf_bytes = generate_pdf_report(sample_analysis)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 0)

    def test_health_check_endpoint(self):
        """Test Flask health check endpoint."""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "healthy")

    def test_test_endpoint(self):
        """Test Flask test connectivity endpoint."""
        response = self.app.get('/test')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")

if __name__ == '__main__':
    unittest.main()

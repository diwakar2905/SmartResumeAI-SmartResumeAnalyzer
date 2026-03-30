from fpdf import FPDF
from datetime import datetime

def sanitize_text(text):
    """Encode text to latin-1, replacing unsupported characters."""
    return text.encode('latin-1', 'replace').decode('latin-1')

class PDF(FPDF):
    def header(self):
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Smart Resume Analyzer Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_text_color(200, 200, 200)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_text_color(0, 0, 0) # Black text for readability on light gray background
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 6, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 10)        
        self.set_text_color(255, 255, 255)
        self.multi_cell(0, 5, sanitize_text(body))
        self.ln()

    def feedback_item(self, item_text, item_type):
        # Set color based on feedback type
        if item_type == 'Strength':
            self.set_text_color(34, 139, 34) # ForestGreen
        elif item_type == 'Suggestion':
            self.set_text_color(255, 165, 0) # Orange
        elif item_type == 'Critical':
            self.set_text_color(220, 20, 60) # Crimson
        else:
            self.set_text_color(255, 255, 255) # Default to white

        self.set_font('Arial', 'B', 10)
        self.multi_cell(0, 5, sanitize_text(f"- {item_text.replace('**', '')}"))
        self.set_text_color(255, 255, 255) # Reset color to white
        self.ln(2)

def get_feedback_type(item_text):
    if any(keyword in item_text for keyword in ['Excellent', 'strong', 'Strength', 'Good']):
        return 'Strength'
    if any(keyword in item_text for keyword in ['Missing', 'weakness', 'Critical', 'Consider']):
        return 'Critical'
    if 'Suggestion' in item_text:
        return 'Suggestion'
    return 'Info'

def generate_pdf_report(data):
    """Generates a PDF report from the analysis data."""
    pdf = PDF()
    pdf.add_page()
    pdf.set_fill_color(17, 24, 39) # Corresponds to --bg-dark: #111827
    pdf.rect(0, 0, 210, 297, 'F') # Draw a full-page background rectangle

    # --- Summary Section ---
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, sanitize_text(f"Analysis for: {data['analysis_metadata']['file_name']}"), 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Overall Score: {data['score']:.0f}/100", 0, 1, 'L')
    pdf.ln(5)

    # --- Feedback Section ---
    pdf.chapter_title('Key Feedback')
    if data.get('feedback'):
        for item in data['feedback']:
            feedback_type = get_feedback_type(item)
            pdf.feedback_item(item, feedback_type)
    else:
        pdf.chapter_body("No specific feedback was generated.")

    # --- Skills Section ---
    pdf.chapter_title('Detected Skills')
    if data.get('skills'):
        for category, skills_list in data['skills'].items():
            if skills_list:
                pdf.set_text_color(255, 255, 255)
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(0, 8, sanitize_text(category), 0, 1, 'L')
                pdf.set_font('Arial', '', 10)
                
                # Create skill tags
                line_x = pdf.get_x()
                for skill in skills_list:
                    skill_width = pdf.get_string_width(skill) + 6
                    if pdf.get_x() + skill_width > pdf.w - pdf.r_margin:
                        pdf.ln(6)
                        pdf.set_x(line_x)

                    pdf.set_fill_color(31, 41, 55) # Corresponds to --card-dark: #1f2937
                    pdf.set_text_color(220, 220, 220)
                    pdf.cell(skill_width, 5, sanitize_text(skill), 1, 0, 'C', 1)
                    pdf.set_x(pdf.get_x() + 2) # Spacing

                pdf.ln(8)
    else:
        pdf.chapter_body("No skills were detected.")

    # --- Metadata Section ---
    pdf.chapter_title('Analysis Metadata')
    meta = data['analysis_metadata']
    meta_text = (
        f"File Size: {meta['file_size'] / 1024:.2f} KB\n"
        f"Text Length: {meta['text_length']} characters\n"
        f"Processing Time: {meta['processing_time']:.2f} seconds\n"
        f"Timestamp: {datetime.fromisoformat(meta['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}"
    )
    pdf.chapter_body(meta_text)

    return pdf.output(dest='S').encode('latin-1')
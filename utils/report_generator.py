from fpdf import FPDF
from datetime import datetime

def sanitize_text(text):
    """Encode text to latin-1, replacing unsupported characters."""
    return text.encode('latin-1', 'replace').decode('latin-1')

class PDF(FPDF):
    def header(self):
        # Top banner with a clean, professional header
        self.set_text_color(15, 118, 110)  # Teal
        self.set_font('helvetica', 'B', 16)
        self.cell(0, 10, 'Smart Resume Analyzer Report', 0, 1, 'C')
        self.set_draw_color(200, 200, 200)
        self.line(10, 22, 200, 22)  # Divider line
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_text_color(150, 150, 150)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_text_color(15, 118, 110)  # Teal
        self.set_font('helvetica', 'B', 12)
        self.set_fill_color(243, 244, 246)  # Light gray background for headers
        self.cell(0, 8, sanitize_text(title), 0, 1, 'L', 1)
        self.ln(3)

    def chapter_body(self, body):
        self.set_font('helvetica', '', 10)        
        self.set_text_color(55, 65, 81)  # Dark gray
        self.multi_cell(0, 5, sanitize_text(body))
        self.ln(2)

    def feedback_item(self, item_text, item_type):
        # Set color based on feedback type (designed for high contrast on light bg)
        if item_type == 'Strength':
            self.set_text_color(21, 128, 61)   # Green-700
        elif item_type == 'Suggestion':
            self.set_text_color(194, 65, 12)   # Orange-700
        elif item_type == 'Critical':
            self.set_text_color(185, 28, 28)   # Red-700
        else:
            self.set_text_color(55, 65, 81)    # Dark gray

        self.set_font('helvetica', 'B', 10)
        # Handle list format display
        bullet = "✓" if item_type == 'Strength' else "•"
        clean_text = item_text.replace('**', '').replace('✅', '').replace('❌', '').replace('⚠️', '').replace('💡', '').strip()
        if clean_text.startswith('•'):
            clean_text = clean_text[1:].strip()
        self.multi_cell(0, 5, sanitize_text(f" {bullet} {clean_text}"))
        self.set_text_color(55, 65, 81)       # Reset color
        self.ln(1.5)

def get_feedback_type(item_text):
    if any(keyword in item_text for keyword in ['Excellent', 'strong', 'Strength', 'Good', '✅']):
        return 'Strength'
    if any(keyword in item_text for keyword in ['Missing', 'weakness', 'Critical', 'Consider', '❌', '⚠️']):
        return 'Critical'
    if 'Suggestion' in item_text or '💡' in item_text:
        return 'Suggestion'
    return 'Info'

def generate_pdf_report(data):
    """Generates a light-themed print-friendly PDF report from analysis data."""
    pdf = PDF()
    pdf.add_page()

    # --- Summary Section ---
    pdf.set_text_color(17, 24, 39)  # Dark slate
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, sanitize_text(f"Analysis for: {data['analysis_metadata']['file_name']}"), 0, 1, 'L')
    pdf.set_font('helvetica', '', 11)
    
    score_val = data.get('score', 0)
    pdf.cell(0, 8, f"Overall Resume Score: {score_val:.1f} / 100", 0, 1, 'L')
    pdf.ln(4)

    # --- Feedback Section ---
    pdf.chapter_title('Key Feedback & Recommendations')
    if data.get('feedback'):
        for item in data['feedback']:
            # Skip overall score summary items in list if they are redundant headings
            if "Overall Assessment" in item or "Score Breakdown" in item:
                # Print them as bold subheaders
                pdf.ln(2)
                pdf.set_text_color(17, 24, 39)
                pdf.set_font('helvetica', 'B', 10)
                pdf.cell(0, 6, sanitize_text(item.replace('**', '')), 0, 1, 'L')
                pdf.set_font('helvetica', '', 10)
                pdf.ln(1)
                continue
            
            feedback_type = get_feedback_type(item)
            pdf.feedback_item(item, feedback_type)
    else:
        pdf.chapter_body("No specific feedback was generated.")
    pdf.ln(4)

    # --- Skills Section ---
    pdf.chapter_title('Detected Skills')
    if data.get('skills'):
        for category, skills_list in data['skills'].items():
            if skills_list:
                pdf.set_text_color(17, 24, 39)
                pdf.set_font('helvetica', 'B', 10)
                pdf.cell(0, 6, sanitize_text(category), 0, 1, 'L')
                pdf.ln(1)
                
                # Create skill tags
                pdf.set_font('helvetica', '', 9)
                line_x = pdf.get_x()
                for skill in skills_list:
                    skill_width = pdf.get_string_width(skill) + 6
                    if pdf.get_x() + skill_width > pdf.w - pdf.r_margin:
                        pdf.ln(6)
                        pdf.set_x(line_x)

                    pdf.set_fill_color(243, 244, 246)  # Light gray tag background
                    pdf.set_text_color(55, 65, 81)     # Dark gray tag text
                    pdf.cell(skill_width, 5, sanitize_text(skill), 1, 0, 'C', 1)
                    pdf.set_x(pdf.get_x() + 2)         # Spacing

                pdf.ln(8)
    else:
        pdf.chapter_body("No skills were detected.")
    pdf.ln(4)

    # --- Metadata Section ---
    pdf.chapter_title('Analysis Metadata')
    meta = data['analysis_metadata']
    meta_text = (
        f"File Name: {meta['file_name']}\n"
        f"File Size: {meta['file_size'] / 1024:.2f} KB\n"
        f"Text Length: {meta['text_length']} characters\n"
        f"Processing Time: {meta['processing_time']:.2f} seconds\n"
        f"Timestamp: {datetime.fromisoformat(meta['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}"
    )
    pdf.chapter_body(meta_text)

    # Output as bytes - Returns a bytes object (fixes the bytearray encode crash)
    return bytes(pdf.output())
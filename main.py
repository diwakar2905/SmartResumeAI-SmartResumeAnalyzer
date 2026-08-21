import os

from parser.resume_parser import extract_text_from_pdf, extract_text_from_docx, extract_basic_info
from utils.scoring import score_resume, WEIGHTS
from utils.feedback import generate_enhanced_feedback
from utils.skill_classifier import classify_skills
from utils.section_extractor import extract_sections

def print_section(title, icon=""):
    """Prints a formatted section header - Section header ko format karke print karte hain."""
    header = f" {icon} {title} " if icon else f" {title} "
    print("\n" + "="*20 + header + "="*20)

def main():
    print("📄 Smart Resume Analyzer (Terminal Version)")
    file_path = input("Enter path to resume (PDF or DOCX): ").strip().replace("\"", "") # Clean up path - Path ko clean karte hain

    if not os.path.exists(file_path):
        print("❌ Error: File does not exist.")
        return

    file_type = "pdf" if file_path.lower().endswith(".pdf") else "docx" if file_path.lower().endswith(".docx") else None
    if not file_type:
        print("❌ Error: Unsupported file format. Please use PDF or DOCX.")
        return

    print("\n🔍 Reading and analyzing resume...")
    text = None
    # --- ROBUST FILE HANDLING --- File handling ko robust banate hain
    try:
        if file_type == "pdf":
            text = extract_text_from_pdf(file_path)
        elif file_type == "docx":
            text = extract_text_from_docx(file_path)
        
        if not text: # Handle case where extraction fails or file is empty - Agar extraction fail ho ya file empty ho
            print("❌ Error: Could not extract text from the file. It might be empty or corrupted.")
            return
    except Exception as e:
        print(f"❌ An unexpected error occurred during file processing: {e}")
        return

    print("✅ Resume parsed successfully.")

    # --- Analysis and Display --- Analysis aur display karte hain
    basic_info = extract_basic_info(text)
    print_section("Basic Info", "👤")
    for key, value in basic_info.items():
        print(f"  {key.capitalize():<12}: {value}")

    # Classify skills using the default dictionary loaded from skills.json - Skills ko classify karte hain skills.json se
    skills = classify_skills(text)
    print_section("Skills Found", "🛠️")
    if not any(skills.values()):
        print("  No specific skills found.")
    else:
        for category, skill_list in skills.items():
            if skill_list:
                print(f"  {category:<25}: {', '.join(skill_list)}")

    sections = extract_sections(text)
    score_data = score_resume(sections, WEIGHTS, text)
    score = score_data["overall_score"]
    feedback = generate_enhanced_feedback(sections, score_data, text)
    
    print_section("Score & Feedback", "⭐")
    print(f"  Resume Score: {score}/100 (Grade: {score_data['grade']})")
    if feedback:
        print("\n  📝 Feedback for Improvement:")
        for item in feedback:
            # Clean markdown highlights from terminal printout
            item_clean = item.replace("**", "").replace("•", "-").strip()
            print(f"     {item_clean}")

if __name__ == '__main__':
    main()
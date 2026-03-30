import re
from typing import Dict, List, Tuple

# Enhanced mapping dictionary for feedback messages - Enhanced feedback messages ke liye mapping dictionary
SECTION_FEEDBACK_MESSAGES = {
    "experience": "Experience: This is the most critical section. Detail your work history with quantifiable achievements and impact metrics.",
    "projects": "Projects: A projects section is crucial for demonstrating practical skills. Include GitHub links, technologies used, and outcomes.",
    "education": "Education: Clearly list your academic background with relevant coursework and achievements.",
    "summary": "Summary: A professional summary helps recruiters understand your profile quickly. Keep it concise and impactful.",
    "certifications": "Certifications: Mention any certifications to highlight specialized knowledge and continuous learning.",
    "skills": "Skills: Organize skills by category and include proficiency levels where appropriate.",
    "achievements": "Achievements: Highlight awards, recognitions, and notable accomplishments."
}

# Industry-specific improvement tips - Industry-specific improvement tips
INDUSTRY_TIPS = {
    "tech": [
        "Include GitHub profile with active repositories",
        "Mention specific programming languages and frameworks",
        "Highlight technical projects with live demos",
        "Include system design and architecture experience",
        "Mention cloud platforms and DevOps tools"
    ],
    "finance": [
        "Quantify financial impact and cost savings",
        "Include relevant certifications (CFA, CPA, etc.)",
        "Highlight risk management experience",
        "Mention financial modeling and analysis skills",
        "Include regulatory compliance knowledge"
    ],
    "marketing": [
        "Include campaign performance metrics",
        "Mention marketing automation tools",
        "Highlight brand development experience",
        "Include social media and digital marketing skills",
        "Mention customer acquisition and retention metrics"
    ],
    "sales": [
        "Include sales targets and achievements",
        "Mention CRM systems and sales methodologies",
        "Highlight client relationship management",
        "Include territory management experience",
        "Mention sales training and mentoring"
    ]
}

# Enhanced improvement tips with specific examples - Specific examples ke saath enhanced improvement tips
ENHANCED_IMPROVEMENT_TIPS = {
    "experience": [
        "Use action verbs to start each bullet point (e.g., 'Developed', 'Implemented', 'Led')",
        "Include quantifiable achievements (e.g., 'Increased sales by 25%', 'Reduced costs by $50K')",
        "Focus on impact and results, not just responsibilities",
        "Use industry-specific keywords and terminology",
        "Include team size and project scope where relevant",
        "Mention technologies, tools, and methodologies used"
    ],
    "projects": [
        "Include live links to deployed projects and GitHub repositories",
        "Mention the complete tech stack and architecture",
        "Describe the problem solved and your unique approach",
        "Highlight any awards, recognition, or user adoption metrics",
        "Include collaboration details and team roles",
        "Mention scalability and performance optimizations"
    ],
    "education": [
        "Include relevant coursework if you're a recent graduate",
        "Mention GPA if it's above 3.5/4.0 or equivalent",
        "List academic achievements, honors, and scholarships",
        "Include relevant certifications and training programs",
        "Mention thesis topics or research projects",
        "Include study abroad or exchange programs if relevant"
    ],
    "summary": [
        "Keep it to 2-3 sentences maximum (30-50 words)",
        "Mention years of experience and key skills upfront",
        "Tailor it to the specific job you're applying for",
        "Avoid generic statements and buzzwords",
        "Include your career objective or target role",
        "Mention unique value proposition or specialization"
    ],
    "certifications": [
        "Include certification dates and expiry if applicable",
        "Mention the issuing organization and credential ID",
        "Focus on industry-recognized certifications",
        "Keep them relevant to your target role",
        "Include ongoing certifications or courses",
        "Mention certification levels or specializations"
    ],
    "skills": [
        "Organize skills by category (Technical, Soft Skills, Tools)",
        "Include proficiency levels (Beginner, Intermediate, Advanced)",
        "Mention years of experience with each skill",
        "Include emerging technologies and trends",
        "Add relevant industry-specific skills",
        "Keep skills current and remove outdated ones"
    ],
    "achievements": [
        "Include specific awards and recognition dates",
        "Mention the awarding organization and criteria",
        "Quantify the impact or significance of achievements",
        "Include industry-specific accolades",
        "Mention leadership awards and team achievements",
        "Include patents, publications, or speaking engagements"
    ]
}

def analyze_content_quality(text: str) -> Dict[str, any]:
    """
    Analyze content quality and provide specific recommendations.
    Content quality analyze karke specific recommendations dete hain.
    
    Returns:
        Dict containing analysis results and recommendations
    """
    analysis = {
        "action_verbs": [],
        "quantifiable_achievements": [],
        "leadership_indicators": [],
        "technical_keywords": [],
        "improvement_areas": []
    }
    
    text_lower = text.lower()
    
    # Action verbs analysis - Action verbs analyze karte hain
    action_verbs = [
        'developed', 'implemented', 'managed', 'led', 'created', 'designed', 'built',
        'improved', 'increased', 'decreased', 'optimized', 'streamlined', 'coordinated',
        'delivered', 'achieved', 'established', 'launched', 'maintained', 'performed',
        'produced', 'reduced', 'resolved', 'supervised', 'trained', 'upgraded'
    ]
    
    found_verbs = [verb for verb in action_verbs if verb in text_lower]
    analysis["action_verbs"] = found_verbs
    
    # Quantifiable achievements analysis - Quantifiable achievements analyze karte hain
    quantifiable_patterns = [
        r'\d+%', r'\d+\s*percent', r'\$\d+', r'\d+\s*dollars', r'\d+\s*users',
        r'\d+\s*customers', r'\d+\s*team\s*members', r'\d+\s*projects',
        r'increased\s+by\s+\d+', r'decreased\s+by\s+\d+', r'reduced\s+by\s+\d+',
        r'improved\s+by\s+\d+', r'grew\s+by\s+\d+', r'expanded\s+by\s+\d+'
    ]
    
    for pattern in quantifiable_patterns:
        matches = re.findall(pattern, text_lower)
        analysis["quantifiable_achievements"].extend(matches)
    
    # Leadership indicators analysis - Leadership indicators analyze karte hain
    leadership_keywords = [
        'led', 'managed', 'supervised', 'directed', 'coordinated', 'oversaw',
        'mentored', 'trained', 'guided', 'facilitated', 'orchestrated'
    ]
    
    found_leadership = [keyword for keyword in leadership_keywords if keyword in text_lower]
    analysis["leadership_indicators"] = found_leadership
    
    # Technical keywords analysis - Technical keywords analyze karte hain
    technical_keywords = [
        'python', 'java', 'javascript', 'react', 'node.js', 'aws', 'docker',
        'kubernetes', 'sql', 'mongodb', 'machine learning', 'ai', 'data science',
        'agile', 'scrum', 'git', 'ci/cd', 'microservices', 'api'
    ]
    
    found_technical = [keyword for keyword in technical_keywords if keyword in text_lower]
    analysis["technical_keywords"] = found_technical
    
    # Identify improvement areas - Improvement areas identify karte hain
    if len(found_verbs) < 5:
        analysis["improvement_areas"].append("Add more action verbs to make your experience more impactful")
    
    if len(analysis["quantifiable_achievements"]) < 3:
        analysis["improvement_areas"].append("Include more quantifiable achievements with specific numbers")
    
    if len(found_leadership) < 2:
        analysis["improvement_areas"].append("Highlight more leadership and management experience")
    
    return analysis

def generate_enhanced_feedback(sections: Dict[str, bool], score_data: Dict[str, any], text: str = "") -> List[str]:
    """
    Generate comprehensive feedback with detailed analysis and actionable recommendations.
    Detailed analysis aur actionable recommendations ke saath comprehensive feedback generate karte hain.
    
    Args:
        sections: Dictionary with section names and presence indicators
        score_data: Enhanced scoring data with breakdown
        text: Full resume text for content analysis
    
    Returns:
        List of detailed feedback messages
    """
    feedback = []
    
    # Overall assessment - Overall assessment
    overall_score = score_data.get("overall_score", 0)
    grade = score_data.get("grade", "D")
    
    feedback.append(f"🎯 **Overall Assessment: {grade} ({overall_score}/100)**")
    
    if overall_score >= 85:
        feedback.append("🏆 **Excellent!** Your resume demonstrates strong professional presentation and comprehensive coverage of key areas.")
    elif overall_score >= 75:
        feedback.append("🚀 **Very Good!** Your resume has a solid foundation with room for strategic improvements.")
    elif overall_score >= 65:
        feedback.append("👍 **Good!** Your resume shows potential but needs targeted enhancements to stand out.")
    elif overall_score >= 55:
        feedback.append("⚠️ **Needs Improvement.** Your resume requires significant work to be competitive.")
    else:
        feedback.append("🚨 **Major Improvements Needed.** Your resume needs substantial restructuring and content enhancement.")
    
    # Score breakdown analysis - Score breakdown analysis
    breakdown = score_data.get("breakdown", {})
    feedback.append("\n📊 **Score Breakdown:**")
    
    for component, score in breakdown.items():
        component_name = component.replace("_", " ").title()
        if score >= 80:
            feedback.append(f"  ✅ {component_name}: {score}/100 (Excellent)")
        elif score >= 65:
            feedback.append(f"  👍 {component_name}: {score}/100 (Good)")
        elif score >= 50:
            feedback.append(f"  ⚠️ {component_name}: {score}/100 (Needs Improvement)")
        else:
            feedback.append(f"  ❌ {component_name}: {score}/100 (Poor)")
    
    # Strengths and weaknesses - Strengths aur weaknesses
    strengths = score_data.get("strengths", [])
    weaknesses = score_data.get("weaknesses", [])
    
    if strengths:
        feedback.append("\n💪 **Key Strengths:**")
        for strength in strengths:
            feedback.append(f"  • {strength}")
    
    if weaknesses:
        feedback.append("\n🔧 **Areas for Improvement:**")
        for weakness in weaknesses:
            feedback.append(f"  • {weakness}")
    
    # Section-specific feedback - Section-specific feedback
    feedback.append("\n📋 **Section-by-Section Analysis:**")
    
    for section, present in sections.items():
        if present:
            feedback.append(f"\n✅ **{section.title()} Section:**")
            if section in ENHANCED_IMPROVEMENT_TIPS:
                tips = ENHANCED_IMPROVEMENT_TIPS[section][:3]  # Top 3 tips
                for tip in tips:
                    feedback.append(f"  💡 {tip}")
        else:
            feedback.append(f"\n❌ **Missing {section.title()} Section:**")
            if section in SECTION_FEEDBACK_MESSAGES:
                feedback.append(f"  ⚠️ {SECTION_FEEDBACK_MESSAGES[section]}")
    
    # Content quality analysis - Content quality analysis
    if text:
        content_analysis = analyze_content_quality(text)
        feedback.append("\n📝 **Content Quality Analysis:**")
        
        if content_analysis["action_verbs"]:
            feedback.append(f"  ✅ Action Verbs Found: {len(content_analysis['action_verbs'])}")
        else:
            feedback.append("  ❌ No action verbs detected")
        
        if content_analysis["quantifiable_achievements"]:
            feedback.append(f"  ✅ Quantifiable Achievements: {len(content_analysis['quantifiable_achievements'])}")
        else:
            feedback.append("  ❌ No quantifiable achievements found")
        
        if content_analysis["leadership_indicators"]:
            feedback.append(f"  ✅ Leadership Indicators: {len(content_analysis['leadership_indicators'])}")
        else:
            feedback.append("  ❌ Limited leadership experience shown")
        
        if content_analysis["technical_keywords"]:
            feedback.append(f"  ✅ Technical Keywords: {len(content_analysis['technical_keywords'])}")
        
        if content_analysis["improvement_areas"]:
            feedback.append("\n🎯 **Content Improvement Priorities:**")
            for area in content_analysis["improvement_areas"]:
                feedback.append(f"  • {area}")
    
    # Industry-specific recommendations - Industry-specific recommendations
    feedback.append("\n🏭 **Industry Best Practices:**")
    feedback.append("  • Use industry-specific keywords and terminology")
    feedback.append("  • Include relevant certifications and training")
    feedback.append("  • Highlight quantifiable achievements and metrics")
    feedback.append("  • Demonstrate continuous learning and skill development")
    feedback.append("  • Show progression and career growth")
    
    # Action plan - Action plan
    feedback.append("\n📈 **Recommended Action Plan:**")
    if overall_score < 70:
        feedback.append("  1. **Immediate (Week 1):** Restructure missing sections and add basic content")
        feedback.append("  2. **Short-term (Week 2-3):** Enhance content with quantifiable achievements")
        feedback.append("  3. **Medium-term (Week 4-6):** Optimize for ATS and industry-specific keywords")
    else:
        feedback.append("  1. **Fine-tune:** Optimize existing content for better impact")
        feedback.append("  2. **Enhance:** Add more quantifiable achievements and metrics")
        feedback.append("  3. **Polish:** Ensure ATS optimization and industry alignment")
    
    return feedback

def generate_feedback(sections, score, weights):
    """
    Legacy function for backward compatibility - Backward compatibility ke liye legacy function.
    """
    # Create a basic score data structure for the enhanced feedback function
    score_data = {
        "overall_score": score, # The numerical score
        "grade": "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D", # A simple grade
        "breakdown": {"section_score": score}, # Basic breakdown
        "strengths": [], # No detailed strengths
        "weaknesses": [] # No detailed weaknesses
    }
    
    # Call the enhanced function with the created score_data dictionary and an empty text string
    return generate_enhanced_feedback(sections, score_data, "")

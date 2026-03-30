import re
from typing import Dict, List, Tuple

def calculate_content_score(text: str) -> float:
    """
    Calculate content quality score based on resume content analysis.
    Resume content ke quality ko analyze karke score calculate karte hain.
    
    Returns:
        float: Content score between 0-100
    """
    score = 0
    
    # Text length analysis - Text length analyze karte hain
    word_count = len(text.split())
    if 200 <= word_count <= 800:
        score += 15  # Optimal length
    elif 100 <= word_count < 200 or 800 < word_count <= 1200:
        score += 10  # Acceptable length
    else:
        score += 5   # Too short or too long
    
    # Action verbs analysis - Action verbs analyze karte hain
    action_verbs = [
        'developed', 'implemented', 'managed', 'led', 'created', 'designed', 'built',
        'improved', 'increased', 'decreased', 'optimized', 'streamlined', 'coordinated',
        'delivered', 'achieved', 'established', 'launched', 'maintained', 'performed',
        'produced', 'reduced', 'resolved', 'supervised', 'trained', 'upgraded'
    ]
    
    text_lower = text.lower()
    action_verb_count = sum(1 for verb in action_verbs if verb in text_lower)
    if action_verb_count >= 8:
        score += 20
    elif action_verb_count >= 5:
        score += 15
    elif action_verb_count >= 3:
        score += 10
    else:
        score += 5
    
    # Quantifiable achievements - Quantifiable achievements check karte hain
    quantifiable_patterns = [
        r'\d+%', r'\d+\s*percent', r'\$\d+', r'\d+\s*dollars', r'\d+\s*users',
        r'\d+\s*customers', r'\d+\s*team\s*members', r'\d+\s*projects',
        r'increased\s+by\s+\d+', r'decreased\s+by\s+\d+', r'reduced\s+by\s+\d+',
        r'improved\s+by\s+\d+', r'grew\s+by\s+\d+', r'expanded\s+by\s+\d+'
    ]
    
    quantifiable_count = 0
    for pattern in quantifiable_patterns:
        quantifiable_count += len(re.findall(pattern, text_lower))
    
    if quantifiable_count >= 5:
        score += 20
    elif quantifiable_count >= 3:
        score += 15
    elif quantifiable_count >= 1:
        score += 10
    else:
        score += 5
    
    # Keyword density analysis - Keyword density analyze karte hain
    professional_keywords = [
        'experience', 'skills', 'project', 'team', 'leadership', 'management',
        'development', 'analysis', 'design', 'implementation', 'strategy',
        'collaboration', 'communication', 'problem-solving', 'innovation'
    ]
    
    keyword_count = sum(1 for keyword in professional_keywords if keyword in text_lower)
    if keyword_count >= 10:
        score += 15
    elif keyword_count >= 7:
        score += 12
    elif keyword_count >= 5:
        score += 10
    else:
        score += 5
    
    return min(score, 100)

def calculate_structure_score(sections: Dict[str, bool]) -> float:
    """
    Calculate structure score based on resume sections and organization.
    Resume sections aur organization ke basis pe structure score calculate karte hain.
    
    Returns:
        float: Structure score between 0-100
    """
    score = 0
    
    # Essential sections - Essential sections check karte hain
    essential_sections = ['summary', 'experience', 'education']
    present_essential = sum(1 for section in essential_sections if sections.get(section, False))
    
    if present_essential == 3:
        score += 30
    elif present_essential == 2:
        score += 20
    elif present_essential == 1:
        score += 10
    
    # Additional valuable sections - Additional valuable sections check karte hain
    valuable_sections = ['projects', 'certifications', 'skills', 'achievements']
    present_valuable = sum(1 for section in valuable_sections if sections.get(section, False))
    
    if present_valuable >= 3:
        score += 20
    elif present_valuable >= 2:
        score += 15
    elif present_valuable >= 1:
        score += 10
    
    # Section order and completeness - Section order aur completeness check karte hain
    if sections.get('summary', False):
        score += 10  # Good to have summary at top
    
    if sections.get('experience', False):
        score += 15  # Experience is crucial
    
    if sections.get('education', False):
        score += 10  # Education is important
    
    return min(score, 100)

def calculate_impact_score(text: str) -> float:
    """
    Calculate impact score based on achievements and results.
    Achievements aur results ke basis pe impact score calculate karte hain.
    
    Returns:
        float: Impact score between 0-100
    """
    score = 0
    
    # Results-oriented language - Results-oriented language check karte hain
    results_keywords = [
        'resulted in', 'led to', 'achieved', 'accomplished', 'delivered',
        'generated', 'produced', 'created', 'established', 'launched',
        'successfully', 'effectively', 'efficiently', 'significantly'
    ]
    
    text_lower = text.lower()
    results_count = sum(1 for keyword in results_keywords if keyword in text_lower)
    
    if results_count >= 8:
        score += 25
    elif results_count >= 5:
        score += 20
    elif results_count >= 3:
        score += 15
    else:
        score += 5
    
    # Specific metrics and numbers - Specific metrics aur numbers check karte hain
    metric_patterns = [
        r'\d+%', r'\$\d+', r'\d+\s*people', r'\d+\s*users', r'\d+\s*customers',
        r'\d+\s*projects', r'\d+\s*team\s*members', r'\d+\s*months', r'\d+\s*years'
    ]
    
    metrics_count = 0
    for pattern in metric_patterns:
        metrics_count += len(re.findall(pattern, text_lower))
    
    if metrics_count >= 10:
        score += 30
    elif metrics_count >= 7:
        score += 25
    elif metrics_count >= 5:
        score += 20
    elif metrics_count >= 3:
        score += 15
    else:
        score += 5
    
    # Leadership and initiative indicators - Leadership aur initiative indicators check karte hain
    leadership_keywords = [
        'led', 'managed', 'supervised', 'directed', 'coordinated', 'oversaw',
        'mentored', 'trained', 'guided', 'facilitated', 'orchestrated'
    ]
    
    leadership_count = sum(1 for keyword in leadership_keywords if keyword in text_lower)
    
    if leadership_count >= 5:
        score += 25
    elif leadership_count >= 3:
        score += 20
    elif leadership_count >= 1:
        score += 15
    else:
        score += 5
    
    return min(score, 100)

def score_resume(sections: Dict[str, bool], weights: Dict[str, int], text: str = "") -> Dict[str, any]:
    """
    Enhanced resume scoring with multiple dimensions and detailed analysis.
    Multiple dimensions aur detailed analysis ke saath enhanced resume scoring.
    
    Args:
        sections: Dictionary with section names as keys and booleans as values
        weights: Dictionary mapping section names to their weights
        text: Full resume text for content analysis
    
    Returns:
        Dict containing overall score and detailed breakdown
    """
    # Calculate different score components - Different score components calculate karte hain
    structure_score = calculate_structure_score(sections)
    content_score = calculate_content_score(text) if text else 0
    impact_score = calculate_impact_score(text) if text else 0
    
    # Calculate section-based score - Section-based score calculate karte hain
    section_score = 0
    for section, present in sections.items():
        if present:
            section_score += weights.get(section, 0)
    
    # Weighted combination - Weighted combination calculate karte hain
    overall_score = (
        section_score * 0.3 +      # 30% weight to sections
        structure_score * 0.25 +   # 25% weight to structure
        content_score * 0.25 +     # 25% weight to content
        impact_score * 0.2         # 20% weight to impact
    )
    
    # Ensure score doesn't exceed 100 - Score 100 se zyada na ho
    overall_score = min(overall_score, 100)
    
    return {
        "overall_score": round(overall_score, 1),
        "breakdown": {
            "section_score": round(section_score, 1),
            "structure_score": round(structure_score, 1),
            "content_score": round(content_score, 1),
            "impact_score": round(impact_score, 1)
        },
        "grade": get_grade(overall_score),
        "strengths": identify_strengths(sections, text),
        "weaknesses": identify_weaknesses(sections, text)
    }

def get_grade(score: float) -> str:
    """Get letter grade based on score - Score ke basis pe letter grade dete hain."""
    if score >= 90:
        return "A+"
    elif score >= 85:
        return "A"
    elif score >= 80:
        return "A-"
    elif score >= 75:
        return "B+"
    elif score >= 70:
        return "B"
    elif score >= 65:
        return "B-"
    elif score >= 60:
        return "C+"
    elif score >= 55:
        return "C"
    elif score >= 50:
        return "C-"
    else:
        return "D"

def identify_strengths(sections: Dict[str, bool], text: str) -> List[str]:
    """Identify resume strengths - Resume ke strengths identify karte hain."""
    strengths = []
    
    if sections.get('experience', False):
        strengths.append("Strong work experience section")
    
    if sections.get('projects', False):
        strengths.append("Includes project portfolio")
    
    if sections.get('certifications', False):
        strengths.append("Professional certifications listed")
    
    if text:
        text_lower = text.lower()
        if len(re.findall(r'\d+%', text_lower)) >= 3:
            strengths.append("Quantifiable achievements present")
        
        if len(re.findall(r'\b(led|managed|supervised)\b', text_lower)) >= 2:
            strengths.append("Leadership experience demonstrated")
    
    return strengths

def identify_weaknesses(sections: Dict[str, bool], text: str) -> List[str]:
    """Identify resume weaknesses - Resume ke weaknesses identify karte hain."""
    weaknesses = []
    
    if not sections.get('summary', False):
        weaknesses.append("Missing professional summary")
    
    if not sections.get('experience', False):
        weaknesses.append("Missing work experience section")
    
    if not sections.get('education', False):
        weaknesses.append("Missing education section")
    
    if text:
        text_lower = text.lower()
        if len(re.findall(r'\d+%', text_lower)) < 2:
            weaknesses.append("Limited quantifiable achievements")
        
        if len(re.findall(r'\b(developed|implemented|created)\b', text_lower)) < 3:
            weaknesses.append("Few action verbs used")
    
    return weaknesses

# Enhanced weightage for each section - Har section ka enhanced weightage
WEIGHTS = {
    "summary": 15,        # Professional summary - Professional summary
    "education": 20,      # Educational background - Educational background
    "experience": 30,     # Work experience (most important) - Work experience (sabse important)
    "projects": 20,       # Project portfolio - Project portfolio
    "certifications": 15, # Professional certifications - Professional certifications
    "skills": 10,         # Skills section - Skills section
    "achievements": 10    # Achievements section - Achievements section
}

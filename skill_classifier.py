import json
import re
import os
from typing import Dict, List, Tuple, Any
from collections import defaultdict

# --- Load skills.json --- skills.json ko load karte hain
# Construct an absolute path to skills.json, assuming it's in the project root.
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) # utils directory
_PROJECT_ROOT = os.path.dirname(_CURRENT_DIR) # Project root
_SKILLS_FILE = os.path.join(_PROJECT_ROOT, 'data', 'skills.json')

try:
    with open(_SKILLS_FILE, 'r', encoding='utf-8') as f:
        # The skills.json file is already in the correct {category: [skills]} format.
        # No transformation is needed.
        default_skill_dict = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    print("⚠️ Warning: 'skills.json' not found or invalid. Using fallback skills.")
    default_skill_dict = {
        "Programming Languages": ["python", "java", "javascript", "c++", "c#", "go", "rust", "swift", "kotlin", "php", "ruby", "scala"],
        "Web & Frontend": ["html", "css", "sass", "react", "angular", "vue", "next.js", "jquery", "bootstrap", "tailwind"],
        "Backend & Frameworks": ["node.js", "express", "django", "flask", "spring", "ruby on rails", ".net", "fastapi"],
        "Databases": ["sql", "mysql", "postgresql", "mongodb", "redis", "sqlite", "oracle", "cassandra", "dynamodb"],
        "Cloud & DevOps": ["aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ansible", "jenkins", "ci/cd", "git", "github actions"],
        "Data Science & ML": ["pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras", "matplotlib", "seaborn", "jupyter", "apache spark"],
        "Software & Tools": ["jira", "confluence", "figma", "postman", "linux", "bash", "powershell"]
    }

# Enhanced skill patterns for better detection - Better detection ke liye enhanced skill patterns
ENHANCED_SKILL_PATTERNS = {
    "Programming Languages": [
        r'\b(python|java|javascript|js|c\+\+|c#|golang|go|rust|swift|kotlin|php|ruby|scala|typescript|ts)\b',
        r'\b(programming|coding|development)\s+(in\s+)?(python|java|javascript|js|c\+\+|c#|golang|go|rust|swift|kotlin|php|ruby|scala|typescript|ts)\b',
        r'\b(wrote|developed|built|created)\s+(in\s+)?(python|java|javascript|js|c\+\+|c#|golang|go|rust|swift|kotlin|php|ruby|scala|typescript|ts)\b'
    ],
    "Web & Frontend": [
        r'\b(html|css|sass|scss|less|react|angular|vue|next\.js|jquery|bootstrap|tailwind|material-ui|mui)\b',
        r'\b(frontend|front-end|front\s+end|web\s+development|ui/ux|user\s+interface)\b',
        r'\b(built|developed|created)\s+(web|frontend|ui)\s+(using\s+)?(html|css|react|angular|vue)\b'
    ],
    "Backend & Frameworks": [
        r'\b(node\.js|nodejs|express|django|flask|spring|ruby\s+on\s+rails|rails|\.net|fastapi|laravel|asp\.net)\b',
        r'\b(backend|back-end|back\s+end|api\s+development|server-side|server\s+side)\b',
        r'\b(developed|built|created)\s+(api|backend|server)\s+(using\s+)?(node|express|django|flask|spring)\b'
    ],
    "Databases": [
        r'\b(sql|mysql|postgresql|postgres|mongodb|redis|sqlite|oracle|cassandra|dynamodb|nosql|database)\b',
        r'\b(database\s+design|data\s+modeling|db\s+administration|data\s+management)\b',
        r'\b(worked\s+with|used|implemented)\s+(sql|mysql|postgresql|mongodb|redis)\b'
    ],
    "Cloud & DevOps": [
        r'\b(aws|amazon\s+web\s+services|azure|gcp|google\s+cloud|docker|kubernetes|k8s|terraform|ansible|jenkins|ci/cd|git|github|gitlab)\b',
        r'\b(devops|cloud\s+computing|infrastructure|deployment|automation|containerization)\b',
        r'\b(deployed|hosted|managed)\s+(on\s+)?(aws|azure|gcp|cloud)\b'
    ],
    "Data Science & ML": [
        r'\b(pandas|numpy|scikit-learn|sklearn|tensorflow|pytorch|keras|matplotlib|seaborn|jupyter|apache\s+spark|spark)\b',
        r'\b(machine\s+learning|ml|data\s+science|artificial\s+intelligence|ai|deep\s+learning|data\s+analysis)\b',
        r'\b(built|developed|trained)\s+(ml|machine\s+learning|ai|data\s+science)\s+(models|algorithms)\b'
    ],
    "Software & Tools": [
        r'\b(jira|confluence|figma|postman|linux|bash|powershell|vscode|visual\s+studio|intellij|eclipse)\b',
        r'\b(project\s+management|agile|scrum|version\s+control|ide|development\s+tools)\b',
        r'\b(used|worked\s+with|managed)\s+(jira|confluence|figma|postman)\b'
    ]
}

# Context indicators for skill confidence - Skill confidence ke liye context indicators
CONTEXT_INDICATORS = {
    "high_confidence": [
        r'\b(proficient|expert|advanced|skilled|experienced)\s+(in|with)\b',
        r'\b(developed|built|created|implemented)\s+(using|with)\b',
        r'\b(worked\s+with|used|applied)\b',
        r'\b(years?\s+of\s+experience)\s+(in|with)\b'
    ],
    "medium_confidence": [
        r'\b(familiar|basic|intermediate|knowledge)\s+(of|with)\b',
        r'\b(learned|studied|trained)\s+(in|on)\b',
        r'\b(used|utilized)\b'
    ],
    "low_confidence": [
        r'\b(heard\s+of|aware\s+of|know\s+about)\b',
        r'\b(maybe|possibly|might)\b'
    ]
}

def analyze_skill_context(text: str, skill: str, position: int) -> float:
    """
    Analyze the context around a skill mention to determine confidence level.
    Skill mention ke around context analyze karke confidence level determine karte hain.
    
    Args:
        text: Full resume text
        skill: The skill being analyzed
        position: Position of skill mention in text
    
    Returns:
        float: Confidence score between 0.0 and 1.0
    """
    # Get context window around skill mention - Skill mention ke around context window get karte hain
    context_start = max(0, position - 100)
    context_end = min(len(text), position + 100)
    context = text[context_start:context_end].lower()
    
    confidence = 0.5  # Default confidence - Default confidence
    
    # Check for high confidence indicators - High confidence indicators check karte hain
    for pattern in CONTEXT_INDICATORS["high_confidence"]:
        if re.search(pattern, context):
            confidence = min(confidence + 0.3, 1.0)
    
    # Check for medium confidence indicators - Medium confidence indicators check karte hain
    for pattern in CONTEXT_INDICATORS["medium_confidence"]:
        if re.search(pattern, context):
            confidence = min(confidence + 0.1, 1.0)
    
    # Check for low confidence indicators - Low confidence indicators check karte hain
    for pattern in CONTEXT_INDICATORS["low_confidence"]:
        if re.search(pattern, context):
            confidence = max(confidence - 0.2, 0.0)
    
    # Check for skill-specific context - Skill-specific context check karte hain
    skill_context_patterns = {
        "python": [r'python\s+script', r'python\s+application', r'python\s+framework'],
        "react": [r'react\s+component', r'react\s+application', r'react\s+hooks'],
        "aws": [r'aws\s+service', r'aws\s+cloud', r'aws\s+deployment'],
        "docker": [r'docker\s+container', r'docker\s+image', r'docker\s+compose'],
        "sql": [r'sql\s+query', r'sql\s+database', r'sql\s+optimization']
    }
    
    if skill.lower() in skill_context_patterns:
        for pattern in skill_context_patterns[skill.lower()]:
            if re.search(pattern, context):
                confidence = min(confidence + 0.2, 1.0)
    
    return confidence

def classify_skills_enhanced(text: str, skill_dict: Dict[str, List[str]] = None) -> Dict[str, Any]:
    """
    Enhanced skill classification with context analysis and confidence scoring.
    Context analysis aur confidence scoring ke saath enhanced skill classification.
    
    Args:
        text: Resume text
        skill_dict: Dictionary of skills by category
    
    Returns:
        Dict containing classified skills with confidence scores and analysis
    """
    if skill_dict is None:
        skill_dict = default_skill_dict
    
    text_lower = text.lower()
    found_skills = {category: [] for category in skill_dict}
    skill_confidence = {}
    skill_contexts = {}
    
    # Method 1: Direct skill matching with context analysis - Context analysis ke saath direct skill matching
    for category, skills in skill_dict.items():
        for skill in skills:
            skill_pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            matches = re.finditer(skill_pattern, text_lower)
            
            for match in matches:
                confidence = analyze_skill_context(text, skill, match.start())
                
                if confidence >= 0.6:  # Only include skills with decent confidence - Sirf decent confidence wale skills include karte hain
                    if skill not in found_skills[category]:
                        found_skills[category].append(skill)
                        skill_confidence[skill] = confidence
                        skill_contexts[skill] = text[max(0, match.start()-50):min(len(text), match.end()+50)]
    
    # Method 2: Pattern-based detection with enhanced patterns - Enhanced patterns ke saath pattern-based detection
    for category, patterns in ENHANCED_SKILL_PATTERNS.items():
        for pattern in patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            
            for match in matches:
                matched_text = match.group()
                # Clean up the match - Match ko clean up karte hain
                if isinstance(matched_text, tuple):
                    matched_text = matched_text[0] if matched_text[0] else matched_text[1]
                
                matched_text = matched_text.strip()
                if matched_text and len(matched_text) > 2:
                    confidence = analyze_skill_context(text, matched_text, match.start())
                    
                    if confidence >= 0.5 and matched_text not in found_skills[category]:
                        found_skills[category].append(matched_text)
                        skill_confidence[matched_text] = confidence
                        skill_contexts[matched_text] = text[max(0, match.start()-50):min(len(text), match.end()+50)]
    
    # Calculate skill statistics - Skill statistics calculate karte hain
    total_skills = sum(len(skills) for skills in found_skills.values())
    avg_confidence = sum(skill_confidence.values()) / len(skill_confidence) if skill_confidence else 0
    
    # Identify skill gaps and recommendations - Skill gaps aur recommendations identify karte hain
    skill_gaps = identify_skill_gaps(found_skills, skill_dict)
    
    return {
        "skills_by_category": found_skills,
        "confidence_scores": skill_confidence,
        "skill_contexts": skill_contexts,
        "statistics": {
            "total_skills": total_skills,
            "average_confidence": round(avg_confidence, 2),
            "categories_with_skills": sum(1 for skills in found_skills.values() if skills),
            "high_confidence_skills": sum(1 for conf in skill_confidence.values() if conf >= 0.8),
            "medium_confidence_skills": sum(1 for conf in skill_confidence.values() if 0.6 <= conf < 0.8),
            "low_confidence_skills": sum(1 for conf in skill_confidence.values() if conf < 0.6)
        },
        "skill_gaps": skill_gaps,
        "recommendations": generate_skill_recommendations(found_skills, skill_gaps)
    }

def identify_skill_gaps(found_skills: Dict[str, List[str]], skill_dict: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Identify missing skills that could strengthen the resume.
    Resume ko strengthen karne wale missing skills identify karte hain.
    
    Returns:
        Dict of missing skills by category
    """
    skill_gaps = {}
    
    for category, skills in skill_dict.items():
        found_in_category = found_skills.get(category, [])
        missing_skills = [skill for skill in skills if skill not in found_in_category]
        
        if missing_skills:
            skill_gaps[category] = missing_skills[:5]  # Top 5 missing skills - Top 5 missing skills
    
    return skill_gaps

def generate_skill_recommendations(found_skills: Dict[str, List[str]], skill_gaps: Dict[str, List[str]]) -> List[str]:
    """
    Generate recommendations for skill improvement.
    Skill improvement ke liye recommendations generate karte hain.
    
    Returns:
        List of skill improvement recommendations
    """
    recommendations = []
    
    # Analyze skill distribution - Skill distribution analyze karte hain
    category_counts = {category: len(skills) for category, skills in found_skills.items()}
    
    # Find categories with few skills - Kam skills wale categories find karte hain
    weak_categories = [cat for cat, count in category_counts.items() if count < 3]
    
    if weak_categories:
        recommendations.append(f"Consider adding more skills in: {', '.join(weak_categories)}")
    
    # Suggest missing high-value skills - Missing high-value skills suggest karte hain
    high_value_skills = {
        "Programming Languages": ["python", "javascript", "java"],
        "Cloud & DevOps": ["aws", "docker", "git"],
        "Data Science & ML": ["python", "pandas", "scikit-learn"],
        "Web & Frontend": ["html", "css", "javascript"]
    }
    
    for category, valuable_skills in high_value_skills.items():
        found_in_category = found_skills.get(category, [])
        missing_valuable = [skill for skill in valuable_skills if skill not in found_in_category]
        
        if missing_valuable:
            recommendations.append(f"Consider adding {', '.join(missing_valuable)} to strengthen your {category} profile")
    
    return recommendations

def classify_skills(text, skill_dict=default_skill_dict):
    """
    Legacy function for backward compatibility - Backward compatibility ke liye legacy function.
    """
    enhanced_result = classify_skills_enhanced(text, skill_dict)
    return enhanced_result["skills_by_category"]

def get_skill_summary(skills_dict):
    """
    Get a summary of skills analysis - Skills analysis ka summary get karte hain.
    """
    total_skills = sum(len(skills) for skills in skills_dict.values())
    categories_with_skills = sum(1 for skills in skills_dict.values() if skills)
    
    return {
        "total_skills": total_skills,
        "categories_with_skills": categories_with_skills,
        "coverage_percentage": (categories_with_skills / len(skills_dict)) * 100 if skills_dict else 0
    }

#!/usr/bin/env python
"""Test script to verify the skill classifier fix"""
import sys
sys.path.insert(0, '.')

from utils.skill_classifier import classify_skills_enhanced

# Sample resume text with various skills
test_text = """
John Doe
Senior Software Engineer

SUMMARY
Experienced software engineer with expertise in Python, Java, and JavaScript. 
Strong background in building scalable backend systems using Node.js and Express.
Proficient in full-stack development with React for frontend and Django for backend.

SKILLS
Programming Languages: Python, Java, JavaScript, TypeScript, C++
Frontend: React, Vue.js, HTML, CSS, Tailwind CSS, Next.js
Backend: Node.js, Express, Django, Flask, Spring Boot, FastAPI
Databases: PostgreSQL, MySQL, MongoDB, Redis
Cloud & DevOps: AWS, Docker, Kubernetes, Jenkins, CI/CD, Git
Data Science: Pandas, NumPy, TensorFlow, Scikit-learn
Mobile: React Native, Flutter
Tools: Jira, Postman, Linux, Bash, Figma

EXPERIENCE
Senior Backend Engineer | Tech Company (2020-Present)
- Developed and maintained backend API using Node.js and Express
- Implemented PostgreSQL database optimization
- Deployed applications on AWS using Docker and Kubernetes
- Managed CI/CD pipelines with Jenkins

Full Stack Developer | StartUp Inc (2018-2020)
- Built responsive web applications using React and Django
- Worked with MongoDB for real-time data management
- Implemented testing using Jest and Pytest
"""

print("Testing skill classifier with fixed category names...\n")

try:
    result = classify_skills_enhanced(test_text)
    
    print("✅ SUCCESS: Skills classified without errors!\n")
    print(f"Total skills found: {result['statistics']['total_skills']}\n")
    
    print("Skills by Category:")
    for category, skills in result['skills_by_category'].items():
        if skills:
            print(f"\n{category}:")
            for skill in skills:
                confidence = result['confidence_scores'].get(skill, 'N/A')
                print(f"  - {skill} (confidence: {confidence})")
    
    print(f"\n\nStatistics:")
    for key, value in result['statistics'].items():
        print(f"  {key}: {value}")
        
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()

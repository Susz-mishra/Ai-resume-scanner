#!/usr/bin/env python3
"""
AI Resume Scanner - Demo Script
This script demonstrates the resume analysis capabilities with sample data.
"""

import json
import os
from datetime import datetime
from resume_analyzer import ResumeAnalyzer
from database import Database

def create_sample_resume():
    """Create a sample resume text for demonstration."""
    sample_text = """
    JOHN DOE
    Software Engineer
    john.doe@email.com | (555) 123-4567 | linkedin.com/in/johndoe | github.com/johndoe
    
    SUMMARY
    Experienced software engineer with 5+ years of expertise in full-stack development, 
    specializing in Python, JavaScript, and cloud technologies. Proven track record of 
    delivering scalable web applications and mentoring junior developers.
    
    TECHNICAL SKILLS
    Programming Languages: Python, JavaScript, Java, C++
    Web Technologies: HTML, CSS, React, Angular, Node.js, Django, Flask
    Databases: MySQL, PostgreSQL, MongoDB, Redis
    Cloud Platforms: AWS, Azure, Google Cloud
    Tools: Git, Docker, Kubernetes, Jenkins, Jira
    Frameworks: TensorFlow, PyTorch, scikit-learn, pandas, numpy
    
    EXPERIENCE
    Senior Software Engineer | TechCorp Inc. | 2020 - Present
    - Led development of microservices architecture using Python and Docker
    - Mentored 3 junior developers and conducted code reviews
    - Implemented CI/CD pipelines with Jenkins and Kubernetes
    
    Software Engineer | StartupXYZ | 2018 - 2020
    - Developed full-stack web applications using React and Node.js
    - Collaborated with cross-functional teams in agile environment
    - Optimized database queries improving performance by 40%
    
    Junior Developer | CodeFactory | 2016 - 2018
    - Built RESTful APIs using Python Flask framework
    - Worked with MySQL and MongoDB databases
    - Participated in code reviews and testing
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology | 2016
    GPA: 3.8/4.0
    
    PROJECTS
    AI Resume Parser - Built machine learning model for resume analysis
    E-commerce Platform - Full-stack application with React and Python
    Data Analytics Dashboard - Real-time analytics using pandas and matplotlib
    
    CERTIFICATIONS
    AWS Certified Developer Associate
    Google Cloud Professional Developer
    Docker Certified Associate
    """
    return sample_text

def save_sample_resume():
    """Save sample resume to a text file."""
    sample_text = create_sample_resume()
    
    # Create uploads directory if it doesn't exist
    os.makedirs('uploads', exist_ok=True)
    
    # Save sample resume
    sample_file = 'uploads/sample_resume.txt'
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write(sample_text)
    
    print(f"✓ Sample resume saved to: {sample_file}")
    return sample_file

def run_demo():
    """Run the complete demo."""
    print("🚀 AI Resume Scanner - Demo Mode")
    print("=" * 50)
    
    try:
        # Initialize components
        analyzer = ResumeAnalyzer()
        db = Database()
        
        # Create and save sample resume
        sample_file = save_sample_resume()
        
        # Analyze the sample resume
        print("\n🔍 Analyzing sample resume...")
        analysis_result = analyzer.analyze_resume(sample_file)
        
        # Display analysis results
        print("\n📊 Analysis Results:")
        print("-" * 30)
        
        # Overall score
        print(f"Overall Score: {analysis_result['overall_score']}/100")
        
        # Experience level
        print(f"Experience Level: {analysis_result['experience_level'].title()}")
        
        # Skills found
        print(f"\nSkills Detected:")
        for category, skills in analysis_result['skills'].items():
            print(f"  {category.replace('_', ' ').title()}: {', '.join(skills)}")
        
        # Contact information
        print(f"\nContact Information:")
        contact = analysis_result['contact_info']
        if contact['email']:
            print(f"  Email: {contact['email']}")
        if contact['phone']:
            print(f"  Phone: {contact['phone']}")
        if contact['linkedin']:
            print(f"  LinkedIn: {contact['linkedin']}")
        if contact['github']:
            print(f"  GitHub: {contact['github']}")
        
        # Education
        print(f"\nEducation:")
        education = analysis_result['education']
        if education['degree']:
            print(f"  Degree: {education['degree']}")
        if education['graduation_year']:
            print(f"  Graduation Year: {education['graduation_year']}")
        
        # Readability metrics
        print(f"\nReadability Metrics:")
        readability = analysis_result['readability']
        print(f"  Flesch Reading Ease: {readability['flesch_reading_ease']}/100")
        print(f"  Grade Level: {readability['flesch_kincaid_grade']}")
        print(f"  Average Sentence Length: {readability['avg_sentence_length']} words")
        print(f"  Average Word Length: {readability['avg_word_length']} characters")
        
        # Key phrases
        print(f"\nKey Phrases:")
        print(f"  {', '.join(analysis_result['key_phrases'][:10])}")
        
        # Store in database
        print(f"\n💾 Storing in database...")
        resume_id = db.add_resume({
            'filename': 'sample_resume.txt',
            'filepath': sample_file,
            'upload_date': datetime.now().isoformat(),
            'analysis_result': analysis_result
        })
        print(f"✓ Resume stored with ID: {resume_id}")
        
        # Get statistics
        stats = db.get_statistics()
        print(f"\n📈 Database Statistics:")
        print(f"  Total Resumes: {stats['total_resumes']}")
        print(f"  Total Shortlists: {stats['total_shortlists']}")
        print(f"  Average Score: {stats['average_score']}")
        
        # Search demonstration
        print(f"\n🔍 Search Demonstration:")
        search_results = db.search_resumes(query="python", skill_filter="python")
        print(f"  Found {len(search_results)} resume(s) with Python skills")
        
        # Create a shortlist
        print(f"\n⭐ Creating sample shortlist...")
        shortlist_id = db.create_shortlist("Top Python Developers", [resume_id])
        print(f"✓ Shortlist created with ID: {shortlist_id}")
        
        print(f"\n🎉 Demo completed successfully!")
        print(f"📱 You can now start the web application with: python start.py")
        print(f"🌐 Open your browser and go to: http://localhost:5000")
        
    except Exception as e:
        print(f"✗ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_demo()





import re
import os
from typing import Dict, List, Any, Optional
import PyPDF2
from docx import Document
from datetime import datetime

class ResumeAnalyzer:
    def __init__(self):
        """Initialize the Resume Analyzer with basic text processing capabilities."""
        # Skill categories expected by UI/templates
        self.skill_categories: Dict[str, List[str]] = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin', 'typescript'],
            'web_technologies': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'node', 'express', 'django', 'flask', 'fastapi', 'spring'],
            'databases': ['mysql', 'postgresql', 'postgres', 'mongodb', 'redis', 'oracle', 'sql server', 'sqlite', 'elasticsearch'],
            'cloud_platforms': ['aws', 'azure', 'google cloud', 'gcp', 'heroku', 'digitalocean'],
            'tools': ['git', 'docker', 'kubernetes', 'jenkins', 'jira', 'confluence', 'slack', 'ci/cd', 'terraform'],
            'frameworks': ['tensorflow', 'pytorch', 'scikit-learn', 'sklearn', 'pandas', 'numpy', 'matplotlib']
        }

        self.experience_keywords = [
            'years', 'experience', 'senior', 'junior', 'lead', 'manager', 'director',
            'intern', 'entry', 'mid-level', 'expert', 'specialist', 'consultant'
        ]

    def extract_text_from_pdf(self, file_path: str) -> str:
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    extracted = page.extract_text() or ''
                    text += extracted + "\n"
                return text.strip()
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""

    def extract_text_from_docx(self, file_path: str) -> str:
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from DOCX: {e}")
            return ""

    def extract_text_from_txt(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            print(f"Error extracting text from TXT: {e}")
            return ""

    def extract_text(self, file_path: str) -> str:
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            return self.extract_text_from_docx(file_path)
        elif file_extension == '.txt':
            return self.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    def extract_contact_info(self, text: str) -> Dict[str, Optional[str]]:
        contact_info: Dict[str, Optional[str]] = {
            'email': None,
            'phone': None,
            'linkedin': None,
            'github': None
        }
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}'
        linkedin_pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+'
        github_pattern = r'(?:https?://)?(?:www\.)?github\.com/[\w-]+'

        m = re.search(email_pattern, text)
        if m:
            contact_info['email'] = m.group()
        m = re.search(phone_pattern, text)
        if m:
            contact_info['phone'] = m.group()
        m = re.search(linkedin_pattern, text, flags=re.IGNORECASE)
        if m:
            contact_info['linkedin'] = m.group()
        m = re.search(github_pattern, text, flags=re.IGNORECASE)
        if m:
            contact_info['github'] = m.group()
        return contact_info

    def extract_skills_categorized(self, text: str) -> Dict[str, List[str]]:
        text_lower = text.lower()
        categorized: Dict[str, List[str]] = {}
        for category, skills in self.skill_categories.items():
            found: List[str] = []
            for s in skills:
                # match whole word occurrences; allow dots in tokens like node.js
                pattern = r'(?:^|[^a-z0-9])' + re.escape(s) + r'(?:[^a-z0-9]|$)'
                if re.search(pattern, text_lower):
                    # Keep canonical form as listed
                    found.append(s)
            if found:
                # Deduplicate while preserving order
                seen = set()
                unique_found = [x for x in found if not (x in seen or seen.add(x))]
                categorized[category] = unique_found
        return categorized

    def infer_experience_level(self, text: str) -> str:
        t = text.lower()
        if re.search(r'\b(?:senior|lead|principal|architect|manager|director|10\+\s*years|7\+\s*years|8\+\s*years|9\+\s*years)\b', t):
            return 'senior'
        if re.search(r'\b(?:3-5\s*years|4-6\s*years|mid|intermediate|experienced|5\+\s*years)\b', t):
            return 'mid'
        return 'entry'

    def extract_education(self, text: str) -> Dict[str, Optional[str]]:
        degree_patterns = [
            r'(Bachelor(?:\s+of)?\s+[^,\n]+)',
            r'(Master(?:\s+of)?\s+[^,\n]+)',
            r'(Ph\.?D\.?\s+in\s+[^,\n]+|Doctorate\s+in\s+[^,\n]+|PhD\s+in\s+[^,\n]+)',
            r'(B\.?Tech\s+in\s+[^,\n]+|M\.?Tech\s+in\s+[^,\n]+)'
        ]
        degree = None
        for p in degree_patterns:
            m = re.search(p, text, flags=re.IGNORECASE)
            if m:
                degree = m.group(1).strip()
                break
        year = None
        m = re.search(r'(20[01]\d|20[2-9]\d|19[89]\d)', text)
        if m:
            year = m.group(1)
        return {
            'degree': degree,
            'institution': None,
            'graduation_year': year
        }

    def calculate_readability(self, text: str) -> Dict[str, float]:
        # Tokenize approximately
        sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
        words = re.findall(r'\b\w+\b', text)
        if not sentences or not words:
            return {
                'flesch_reading_ease': 0.0,
                'flesch_kincaid_grade': 0.0,
                'avg_sentence_length': 0.0,
                'avg_word_length': 0.0
            }
        avg_sentence_len = len(words) / max(1, len(sentences))
        avg_word_len = sum(len(w) for w in words) / len(words)
        # Approximate Flesch using word length as proxy for syllables
        flesch = 206.835 - (1.015 * avg_sentence_len) - (84.6 * (avg_word_len / 3.0))
        fk = (0.39 * avg_sentence_len) + (11.8 * (avg_word_len / 3.0)) - 15.59
        return {
            'flesch_reading_ease': round(max(0.0, min(100.0, flesch)), 2),
            'flesch_kincaid_grade': round(max(0.0, fk), 2),
            'avg_sentence_length': round(avg_sentence_len, 2),
            'avg_word_length': round(avg_word_len, 2)
        }

    def extract_key_phrases(self, text: str, top_k: int = 10) -> List[str]:
        words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9\-]+\b', text.lower())
        stop = {
            'the','a','an','and','or','but','in','on','at','to','for','of','with','by','is','are','was','were','be','been','have','has','had',
            'do','does','did','will','would','could','should','may','might','can','this','that','these','those','i','you','he','she','it','we','they',
            'me','him','her','us','them','from','as','per','etc','about'
        }
        freq: Dict[str, int] = {}
        for w in words:
            if len(w) <= 3 or w in stop:
                continue
            freq[w] = freq.get(w, 0) + 1
        ranked = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [w for w, _ in ranked[:top_k]]

    def calculate_overall_score(self, skills: Dict[str, List[str]], experience_level: str, education: Dict[str, Optional[str]], readability: Dict[str, float]) -> float:
        score = 0.0
        total_skills = sum(len(v) for v in skills.values())
        score += min(100, total_skills * 8) * 0.4  # up to 40 points
        exp_map = {'entry': 60, 'mid': 80, 'senior': 100}
        score += exp_map.get(experience_level, 60) * 0.3  # up to 30 points
        score += (80 if education.get('degree') else 40) * 0.2  # up to 16 points
        score += min(100.0, readability.get('flesch_reading_ease', 0.0)) * 0.1  # up to 10 points
        return round(score, 2)

    def analyze_resume(self, file_path: str) -> Dict[str, Any]:
        text = self.extract_text(file_path)
        if not text:
            raise Exception("No text content found in the file")

        contact_info = self.extract_contact_info(text)
        skills_categorized = self.extract_skills_categorized(text)
        experience_level = self.infer_experience_level(text)  # 'entry' | 'mid' | 'senior'
        education = self.extract_education(text)
        readability = self.calculate_readability(text)
        key_phrases = self.extract_key_phrases(text)
        overall_score = self.calculate_overall_score(skills_categorized, experience_level, education, readability)

        analysis_result: Dict[str, Any] = {
            'text_content': (text[:1000] + '...') if len(text) > 1000 else text,
            'contact_info': contact_info,
            'skills': skills_categorized,
            'experience_level': experience_level,
            'education': education,
            'readability': readability,
            'key_phrases': key_phrases,
            'overall_score': overall_score,
            'word_count': len(text.split()),
            'analysis_timestamp': datetime.now().isoformat()
        }
        return analysis_result

    def search_resumes(self, resumes: List[Dict], query: str, filters: Optional[Dict] = None) -> List[Dict]:
        if not query and not filters:
            return resumes
        results: List[Dict] = []
        q = (query or '').lower()
        for r in resumes:
            score = 0
            text = r.get('analysis_result', {}).get('text_content', '').lower()
            if q and q in text:
                score += 10
            if q:
                skills = r.get('analysis_result', {}).get('skills', {})
                for _, lst in skills.items():
                    if any(q in s.lower() for s in lst):
                        score += 10
            if filters:
                if 'min_score' in filters and r.get('analysis_result', {}).get('overall_score', 0) < filters['min_score']:
                    continue
                if 'experience_level' in filters and r.get('analysis_result', {}).get('experience_level') != filters['experience_level']:
                    continue
            if score > 0 or not q:
                r_copy = dict(r)
                r_copy['search_score'] = score
                results.append(r_copy)
        results.sort(key=lambda x: x.get('search_score', 0), reverse=True)
        return results

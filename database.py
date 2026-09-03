import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

class Database:
    def __init__(self, db_file='resume_database.json'):
        self.db_file = db_file
        self.data = self.load_data()
    
    def load_data(self) -> Dict[str, Any]:
        """Load data from JSON file"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        # Initialize with default structure
        return {
            'resumes': [],
            'shortlists': [],
            'next_resume_id': 1,
            'next_shortlist_id': 1
        }
    
    def save_data(self):
        """Save data to JSON file"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def add_resume(self, resume_data: Dict[str, Any]) -> int:
        """Add a new resume to the database"""
        resume_id = self.data['next_resume_id']
        self.data['next_resume_id'] += 1
        
        resume = {
            'id': resume_id,
            'filename': resume_data.get('filename', ''),
            'filepath': resume_data.get('filepath', ''),
            'upload_date': resume_data.get('upload_date', datetime.now().isoformat()),
            'analysis_result': resume_data.get('analysis_result', {}),
            'status': 'active',
            'tags': [],
            'notes': ''
        }
        
        self.data['resumes'].append(resume)
        self.save_data()
        return resume_id
    
    def get_resume(self, resume_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific resume by ID"""
        for resume in self.data['resumes']:
            if resume['id'] == resume_id:
                return resume
        return None
    
    def get_all_resumes(self) -> List[Dict[str, Any]]:
        """Get all resumes"""
        return self.data['resumes'].copy()
    
    def get_recent_resumes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent resumes sorted by upload date"""
        sorted_resumes = sorted(
            self.data['resumes'],
            key=lambda x: x.get('upload_date', ''),
            reverse=True
        )
        return sorted_resumes[:limit]
    
    def update_resume(self, resume_id: int, updates: Dict[str, Any]) -> bool:
        """Update a resume with new data"""
        resume = self.get_resume(resume_id)
        if not resume:
            return False
        
        for key, value in updates.items():
            if key in resume:
                resume[key] = value
        
        self.save_data()
        return True
    
    def delete_resume(self, resume_id: int) -> bool:
        """Delete a resume from the database"""
        resume = self.get_resume(resume_id)
        if not resume:
            return False
        
        # Remove from database
        self.data['resumes'] = [r for r in self.data['resumes'] if r['id'] != resume_id]
        
        # Remove from shortlists
        for shortlist in self.data['shortlists']:
            if resume_id in shortlist.get('resume_ids', []):
                shortlist['resume_ids'].remove(resume_id)
        
        # Try to delete the actual file
        try:
            if os.path.exists(resume['filepath']):
                os.remove(resume['filepath'])
        except Exception as e:
            print(f"Error deleting file {resume['filepath']}: {e}")
        
        self.save_data()
        return True
    
    def search_resumes(self, query: str = '', skill_filter: str = '', experience_filter: str = '') -> List[Dict[str, Any]]:
        """Search resumes based on various criteria"""
        results = []
        query_lower = query.lower()
        skill_filter_lower = skill_filter.lower()
        experience_filter_lower = experience_filter.lower()
        
        for resume in self.data['resumes']:
            score = 0
            analysis = resume.get('analysis_result', {})
            
            # Text search
            if query:
                text_content = analysis.get('text_content', '').lower()
                if query_lower in text_content:
                    score += 10
            
            # Skill filter
            if skill_filter:
                skills = analysis.get('skills', {})
                for category, skill_list in skills.items():
                    if skill_filter_lower in [skill.lower() for skill in skill_list]:
                        score += 15
            
            # Experience filter
            if experience_filter:
                exp_level = analysis.get('experience_level', '').lower()
                if experience_filter_lower == exp_level:
                    score += 20
            
            # If no filters applied, include all resumes
            if not query and not skill_filter and not experience_filter:
                score = 1
            
            if score > 0:
                resume_copy = resume.copy()
                resume_copy['search_score'] = score
                results.append(resume_copy)
        
        # Sort by search score
        results.sort(key=lambda x: x.get('search_score', 0), reverse=True)
        return results
    
    def create_shortlist(self, name: str, resume_ids: List[int]) -> int:
        """Create a new shortlist"""
        shortlist_id = self.data['next_shortlist_id']
        self.data['next_shortlist_id'] += 1
        
        shortlist = {
            'id': shortlist_id,
            'name': name,
            'resume_ids': resume_ids,
            'created_date': datetime.now().isoformat(),
            'description': ''
        }
        
        self.data['shortlists'].append(shortlist)
        self.save_data()
        return shortlist_id
    
    def get_shortlist(self, shortlist_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific shortlist by ID"""
        for shortlist in self.data['shortlists']:
            if shortlist['id'] == shortlist_id:
                return shortlist
        return None
    
    def get_all_shortlists(self) -> List[Dict[str, Any]]:
        """Get all shortlists"""
        return self.data['shortlists'].copy()
    
    def update_shortlist(self, shortlist_id: int, updates: Dict[str, Any]) -> bool:
        """Update a shortlist"""
        shortlist = self.get_shortlist(shortlist_id)
        if not shortlist:
            return False
        
        for key, value in updates.items():
            if key in shortlist:
                shortlist[key] = value
        
        self.save_data()
        return True
    
    def delete_shortlist(self, shortlist_id: int) -> bool:
        """Delete a shortlist"""
        shortlist = self.get_shortlist(shortlist_id)
        if not shortlist:
            return False
        
        self.data['shortlists'] = [s for s in self.data['shortlists'] if s['id'] != shortlist_id]
        self.save_data()
        return True
    
    def get_shortlist_resumes(self, shortlist_id: int) -> List[Dict[str, Any]]:
        """Get all resumes in a specific shortlist"""
        shortlist = self.get_shortlist(shortlist_id)
        if not shortlist:
            return []
        
        resume_ids = shortlist.get('resume_ids', [])
        resumes = []
        
        for resume_id in resume_ids:
            resume = self.get_resume(resume_id)
            if resume:
                resumes.append(resume)
        
        return resumes
    
    def add_resume_to_shortlist(self, shortlist_id: int, resume_id: int) -> bool:
        """Add a resume to a shortlist"""
        shortlist = self.get_shortlist(shortlist_id)
        if not shortlist:
            return False
        
        if resume_id not in shortlist.get('resume_ids', []):
            shortlist['resume_ids'].append(resume_id)
            self.save_data()
        
        return True
    
    def remove_resume_from_shortlist(self, shortlist_id: int, resume_id: int) -> bool:
        """Remove a resume from a shortlist"""
        shortlist = self.get_shortlist(shortlist_id)
        if not shortlist:
            return False
        
        if resume_id in shortlist.get('resume_ids', []):
            shortlist['resume_ids'].remove(resume_id)
            self.save_data()
        
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get overall statistics about the resume database"""
        total_resumes = len(self.data['resumes'])
        total_shortlists = len(self.data['shortlists'])
        
        # Skills distribution
        skills_count = {}
        experience_distribution = {'entry': 0, 'mid': 0, 'senior': 0}
        education_distribution = {'bachelor': 0, 'master': 0, 'phd': 0, 'other': 0}
        
        for resume in self.data['resumes']:
            analysis = resume.get('analysis_result', {})
            
            # Count skills
            skills = analysis.get('skills', {})
            for category, skill_list in skills.items():
                for skill in skill_list:
                    skills_count[skill] = skills_count.get(skill, 0) + 1
            
            # Count experience levels
            exp_level = analysis.get('experience_level', 'entry')
            experience_distribution[exp_level] = experience_distribution.get(exp_level, 0) + 1
            
            # Count education levels
            degree = analysis.get('education', {}).get('degree', '').lower()
            if 'bachelor' in degree:
                education_distribution['bachelor'] += 1
            elif 'master' in degree:
                education_distribution['master'] += 1
            elif 'phd' in degree:
                education_distribution['phd'] += 1
            else:
                education_distribution['other'] += 1
        
        # Top skills
        top_skills = sorted(skills_count.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Average scores
        scores = [r.get('analysis_result', {}).get('overall_score', 0) for r in self.data['resumes']]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        return {
            'total_resumes': total_resumes,
            'total_shortlists': total_shortlists,
            'top_skills': top_skills,
            'experience_distribution': experience_distribution,
            'education_distribution': education_distribution,
            'average_score': round(avg_score, 2),
            'last_updated': datetime.now().isoformat()
        }
    
    def export_data(self, format_type: str = 'json') -> str:
        """Export database data in specified format"""
        if format_type == 'json':
            return json.dumps(self.data, indent=2, ensure_ascii=False, default=str)
        elif format_type == 'csv':
            # Simple CSV export for resumes
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow(['ID', 'Filename', 'Upload Date', 'Overall Score', 'Experience Level', 'Skills'])
            
            # Write data
            for resume in self.data['resumes']:
                analysis = resume.get('analysis_result', {})
                skills = analysis.get('skills', {})
                all_skills = ', '.join([skill for skill_list in skills.values() for skill in skill_list])
                
                writer.writerow([
                    resume['id'],
                    resume['filename'],
                    resume['upload_date'],
                    analysis.get('overall_score', 0),
                    analysis.get('experience_level', ''),
                    all_skills
                ])
            
            return output.getvalue()
        
        return "Unsupported format"
    
    def backup_database(self, backup_file: str = None) -> str:
        """Create a backup of the database"""
        if not backup_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = f'backup_{timestamp}.json'
        
        try:
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False, default=str)
            return backup_file
        except Exception as e:
            raise Exception(f"Backup failed: {e}")
    
    def restore_database(self, backup_file: str) -> bool:
        """Restore database from backup"""
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            # Validate backup data structure
            required_keys = ['resumes', 'shortlists', 'next_resume_id', 'next_shortlist_id']
            if not all(key in backup_data for key in required_keys):
                raise Exception("Invalid backup file format")
            
            self.data = backup_data
            self.save_data()
            return True
            
        except Exception as e:
            raise Exception(f"Restore failed: {e}")





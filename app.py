from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
import json
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime
from resume_analyzer import ResumeAnalyzer
from database import Database

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize components
db = Database()
analyzer = ResumeAnalyzer()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save file
        file.save(filepath)
        
        # Analyze resume
        try:
            analysis_result = analyzer.analyze_resume(filepath)
            
            # Store in database
            resume_id = db.add_resume({
                'filename': filename,
                'filepath': filepath,
                'upload_date': datetime.now().isoformat(),
                'analysis_result': analysis_result
            })
            
            return jsonify({
                'success': True,
                'resume_id': resume_id,
                'analysis': analysis_result
            })
            
        except Exception as e:
            return jsonify({'error': f'Analysis failed: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/resumes')
def list_resumes():
    resumes = db.get_all_resumes()
    return render_template('resumes.html', resumes=resumes)

@app.route('/resume/<int:resume_id>')
def view_resume(resume_id):
    resume = db.get_resume(resume_id)
    if not resume:
        flash('Resume not found', 'error')
        return redirect(url_for('list_resumes'))
    
    return render_template('resume_detail.html', resume=resume)

@app.route('/api/resumes')
def api_resumes():
    resumes = db.get_all_resumes()
    return jsonify(resumes)

@app.route('/api/resume/<int:resume_id>')
def api_resume(resume_id):
    resume = db.get_resume(resume_id)
    if not resume:
        return jsonify({'error': 'Resume not found'}), 404
    return jsonify(resume)

# New: delete resume by ID
@app.route('/api/resume/<int:resume_id>', methods=['DELETE'])
def api_delete_resume(resume_id):
    try:
        deleted = db.delete_resume(resume_id)
        if not deleted:
            return jsonify({'error': 'Resume not found'}), 404
        return jsonify({'success': True, 'deleted_id': resume_id}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to delete resume: {str(e)}'}), 500

@app.route('/search')
def search_resumes():
    query = request.args.get('q', '')
    skill_filter = request.args.get('skill', '')
    experience_filter = request.args.get('experience', '')
    
    resumes = db.search_resumes(query, skill_filter, experience_filter)
    return render_template('search_results.html', resumes=resumes, query=query)

@app.route('/shortlist', methods=['GET', 'POST'])
def shortlist_resumes():
    if request.method == 'POST':
        resume_ids = request.form.getlist('resume_ids')
        shortlist_name = request.form.get('shortlist_name', 'Default Shortlist')
        
        db.create_shortlist(shortlist_name, resume_ids)
        flash(f'Shortlist "{shortlist_name}" created successfully!', 'success')
        return redirect(url_for('shortlist_resumes'))
    
    shortlists = db.get_all_shortlists()
    return render_template('shortlist.html', shortlists=shortlists)

@app.route('/dashboard')
def dashboard():
    stats = db.get_statistics()
    recent_resumes = db.get_recent_resumes(5)
    return render_template('dashboard.html', stats=stats, recent_resumes=recent_resumes)

@app.route('/api/statistics')
def api_statistics():
    stats = db.get_statistics()
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

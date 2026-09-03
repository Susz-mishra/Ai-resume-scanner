# AI Resume Scanner

A fully functional AI-powered resume analysis and candidate shortlisting web application designed for campus recruitment and HR professionals.

## 🚀 Features

### Core Functionality
- **AI-Powered Resume Analysis**: Advanced NLP and machine learning algorithms extract key information from resumes
- **Multi-Format Support**: Handles PDF, DOCX, DOC, and TXT files
- **Intelligent Skill Extraction**: Automatically identifies technical skills, programming languages, frameworks, and tools
- **Experience Level Detection**: Classifies candidates as Entry, Mid, or Senior level
- **Education Analysis**: Extracts degree information and graduation details
- **Contact Information Extraction**: Automatically finds email, phone, LinkedIn, and GitHub profiles
- **Readability Scoring**: Calculates Flesch Reading Ease and Flesch-Kincaid Grade Level

### Web Application Features
- **Modern UI/UX**: Beautiful, responsive interface built with Bootstrap 5
- **Drag & Drop Upload**: Intuitive resume upload with drag-and-drop support
- **Smart Search & Filtering**: Find candidates by skills, experience level, or text content
- **Candidate Shortlisting**: Create and manage shortlists for different positions
- **Comprehensive Dashboard**: Analytics and statistics about your resume database
- **Export Functionality**: Export shortlists and data in CSV format
- **Real-time Analysis**: Instant resume processing and scoring

### Technical Features
- **Scalable Architecture**: Built with Flask for easy deployment and scaling
- **JSON Database**: Lightweight, file-based storage system
- **RESTful API**: Clean API endpoints for integration
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Cross-Platform**: Runs on Windows, macOS, and Linux

## 🛠️ Technology Stack

- **Backend**: Python 3.8+, Flask
- **AI/ML**: NLTK, spaCy, scikit-learn
- **Document Processing**: PyPDF2, python-docx
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: JSON-based file storage
- **Dependencies**: See `requirements.txt`

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "Resume scanner"
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download NLTK Data
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

## 🎯 Usage

### Starting the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

### Basic Workflow

1. **Upload Resumes**
   - Navigate to the home page
   - Drag and drop resume files or click to browse
   - Supported formats: PDF, DOCX, DOC, TXT
   - Maximum file size: 16MB

2. **View Analysis Results**
   - Each resume gets automatically analyzed
   - View detailed breakdowns of skills, experience, and scores
   - Check contact information and readability metrics

3. **Search and Filter**
   - Use the search functionality to find specific candidates
   - Filter by skills, experience level, or minimum score
   - Sort results by relevance or score

4. **Create Shortlists**
   - Group top candidates into shortlists
   - Add descriptions and manage multiple lists
   - Export shortlists for further processing

5. **Monitor Progress**
   - Dashboard shows overall statistics
   - Track total resumes, average scores, and skill distributions
   - View recent uploads and system activity

## 📊 API Endpoints

### Resume Management
- `GET /api/resumes` - List all resumes
- `GET /api/resume/<id>` - Get specific resume details
- `POST /upload` - Upload new resume
- `DELETE /api/resume/<id>` - Delete resume

### Shortlist Management
- `GET /api/shortlists` - List all shortlists
- `GET /api/shortlist/<id>` - Get shortlist details
- `POST /shortlist` - Create new shortlist
- `PUT /api/shortlist/<id>` - Update shortlist
- `DELETE /api/shortlist/<id>` - Delete shortlist

### Analytics
- `GET /api/statistics` - Get system statistics
- `GET /dashboard` - Dashboard view

## 🔧 Configuration

### Environment Variables
- `FLASK_SECRET_KEY`: Secret key for session management
- `UPLOAD_FOLDER`: Directory for storing uploaded files
- `MAX_CONTENT_LENGTH`: Maximum file size (default: 16MB)

### Customization
- Modify `resume_analyzer.py` to add new skill categories
- Update scoring algorithms in the analyzer
- Customize UI themes in `templates/base.html`

## 📁 Project Structure

```
Resume scanner/
├── app.py                 # Main Flask application
├── resume_analyzer.py     # AI resume analysis engine
├── database.py           # Database management
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   ├── index.html      # Home page
│   ├── dashboard.html  # Dashboard
│   ├── resumes.html    # Resume listing
│   ├── resume_detail.html # Resume details
│   ├── search_results.html # Search results
│   └── shortlist.html  # Shortlist management
├── uploads/            # Uploaded resume files
└── resume_database.json # Database file
```

## 🚀 Deployment

### Production Deployment
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🔒 Security Features

- File type validation
- File size limits
- Secure filename handling
- Input sanitization
- Session management

## 📈 Performance

- Optimized text processing algorithms
- Efficient file handling
- Responsive UI with minimal loading times
- Scalable architecture for large datasets

## 🐛 Troubleshooting

### Common Issues

1. **NLTK Data Not Found**
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
   ```

2. **File Upload Errors**
   - Check file format (PDF, DOCX, DOC, TXT only)
   - Ensure file size < 16MB
   - Verify upload directory permissions

3. **Analysis Failures**
   - Check if resume contains extractable text
   - Verify all dependencies are installed
   - Check console logs for specific errors

### Logs and Debugging
- Enable debug mode in `app.py` for detailed error messages
- Check console output for Python errors
- Monitor browser developer console for JavaScript issues

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- NLTK team for natural language processing capabilities
- Bootstrap team for the responsive UI framework
- Flask community for the web framework
- Open source contributors for various Python packages

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the code comments for implementation details

## 🔮 Future Enhancements

- Integration with job boards and ATS systems
- Advanced machine learning models for better analysis
- Multi-language support
- Cloud storage integration
- Real-time collaboration features
- Advanced reporting and analytics
- Mobile app development

---

**Built with ❤️ for the recruitment community**





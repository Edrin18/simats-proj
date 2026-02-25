# Create a deployment README
readme = '''# SIMATS Hub - Student Project Repository

A simple web platform for SIMATS students to share projects and notes. No login required!

## Features

- 📁 **Project Repository**: Upload/download projects with reports and PPTs
- 📚 **Notes Exchange**: Share unit-wise study notes
- ✅ **Verification System**: Students verify if projects work
- 🔍 **Search**: Find by course code, subject, or professor

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML + Tailwind CSS
- **Hosting**: Render (Free)

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Open http://localhost:5000
```

## Deployment to Render

1. Push code to GitHub
2. Connect to Render
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`
5. Done!

## File Structure

```
simats-hub/
├── app.py                 # Main Flask app
├── requirements.txt       # Dependencies
├── simats_hub.db         # Database (auto-created)
├── static/uploads/       # Uploaded files
│   ├── projects/
│   ├── reports/
│   ├── ppts/
│   └── notes/
└── templates/            # HTML templates
    ├── base.html
    ├── index.html
    ├── projects.html
    ├── project_detail.html
    ├── notes.html
    ├── upload_project.html
    ├── upload_note.html
    ├── request_project.html
    └── search.html
```

## Notes

- No authentication required - anyone can upload/download
- Files stored locally (use AWS S3 for production)
- SQLite database (use PostgreSQL for high traffic)
- Max file size: 50MB

Made with ❤️ for SIMATS students
'''

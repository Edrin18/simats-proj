from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'studyshare-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studyshare.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

UPLOAD_FOLDERS = {
    'project': 'static/uploads/projects',
    'report': 'static/uploads/reports',
    'ppt': 'static/uploads/ppts',
    'note': 'static/uploads/notes'
}

for folder in UPLOAD_FOLDERS.values():
    os.makedirs(folder, exist_ok=True)

db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), nullable=False, index=True)
    subject_name = db.Column(db.String(100), nullable=False)
    professor = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    tech_stack = db.Column(db.String(200), nullable=False)
    github_link = db.Column(db.String(500))
    project_file = db.Column(db.String(200))
    report_file = db.Column(db.String(200))
    ppt_file = db.Column(db.String(200))
    demo_video = db.Column(db.String(500))
    uploader_name = db.Column(db.String(100), nullable=False)
    uploader_roll = db.Column(db.String(20), nullable=False)
    downloads = db.Column(db.Integer, default=0)
    verified_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), nullable=False, index=True)
    subject_name = db.Column(db.String(100), nullable=False)
    unit_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(200), nullable=False)
    uploader_name = db.Column(db.String(100), nullable=False)
    rating_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Verification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    worked = db.Column(db.Boolean, default=True)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    recent_projects = Project.query.order_by(Project.created_at.desc()).limit(6).all()
    recent_notes = Note.query.order_by(Note.created_at.desc()).limit(6).all()
    stats = {
        'total_projects': Project.query.count(),
        'total_notes': Note.query.count()
    }
    return render_template('index.html', projects=recent_projects, notes=recent_notes, stats=stats)

@app.route('/projects')
def projects():
    page = request.args.get('page', 1, type=int)
    course_filter = request.args.get('course', '')
    sem_filter = request.args.get('semester', type=int)
    prof_filter = request.args.get('professor', '')
    
    query = Project.query
    
    if course_filter:
        query = query.filter(Project.course_code.ilike(f'%{course_filter}%'))
    if sem_filter:
        query = query.filter_by(semester=sem_filter)
    if prof_filter:
        query = query.filter(Project.professor.ilike(f'%{prof_filter}%'))
    
    projects = query.order_by(Project.created_at.desc()).paginate(page=page, per_page=12)
    return render_template('projects.html', projects=projects, 
                         course_filter=course_filter, sem_filter=sem_filter, prof_filter=prof_filter)

@app.route('/project/<int:id>')
def project_detail(id):
    project = Project.query.get_or_404(id)
    verifications = Verification.query.filter_by(project_id=id).order_by(Verification.created_at.desc()).limit(5).all()
    return render_template('project_detail.html', project=project, verifications=verifications)

@app.route('/upload_project', methods=['GET', 'POST'])
def upload_project():
    if request.method == 'POST':
        roll = request.form['uploader_roll']
        
        project_file = request.files.get('project_file')
        report_file = request.files.get('report_file')
        ppt_file = request.files.get('ppt_file')
        
        project_filename = None
        report_filename = None
        ppt_filename = None
        
        if project_file and project_file.filename:
            project_filename = secure_filename(f"{roll}_{project_file.filename}")
            project_file.save(os.path.join(UPLOAD_FOLDERS['project'], project_filename))
        
        if report_file and report_file.filename:
            report_filename = secure_filename(f"{roll}_{report_file.filename}")
            report_file.save(os.path.join(UPLOAD_FOLDERS['report'], report_filename))
        
        if ppt_file and ppt_file.filename:
            ppt_filename = secure_filename(f"{roll}_{ppt_file.filename}")
            ppt_file.save(os.path.join(UPLOAD_FOLDERS['ppt'], ppt_filename))
        
        project = Project(
            course_code=request.form['course_code'].upper(),
            subject_name=request.form['subject_name'],
            professor=request.form['professor'],
            semester=int(request.form['semester']),
            description=request.form['description'],
            tech_stack=request.form['tech_stack'],
            github_link=request.form.get('github_link', ''),
            demo_video=request.form.get('demo_video', ''),
            project_file=project_filename,
            report_file=report_filename,
            ppt_file=ppt_filename,
            uploader_name=request.form['uploader_name'],
            uploader_roll=roll
        )
        
        db.session.add(project)
        db.session.commit()
        flash('Project uploaded successfully!', 'success')
        return redirect(url_for('project_detail', id=project.id))
    
    return render_template('upload_project.html')

@app.route('/notes')
def notes():
    page = request.args.get('page', 1, type=int)
    course_filter = request.args.get('course', '')
    
    query = Note.query
    if course_filter:
        query = query.filter(Note.course_code.ilike(f'%{course_filter}%'))
    
    notes = query.order_by(Note.created_at.desc()).paginate(page=page, per_page=12)
    return render_template('notes.html', notes=notes, course_filter=course_filter)

@app.route('/upload_note', methods=['GET', 'POST'])
def upload_note():
    if request.method == 'POST':
        roll = request.form['uploader_roll']
        
        note_file = request.files['note_file']
        if note_file and note_file.filename:
            filename = secure_filename(f"{roll}_{note_file.filename}")
            note_file.save(os.path.join(UPLOAD_FOLDERS['note'], filename))
            
            note = Note(
                course_code=request.form['course_code'].upper(),
                subject_name=request.form['subject_name'],
                unit_number=int(request.form['unit_number']),
                title=request.form['title'],
                description=request.form.get('description', ''),
                file_path=filename,
                uploader_name=request.form['uploader_name']
            )
            
            db.session.add(note)
            db.session.commit()
            flash('Notes uploaded successfully!', 'success')
            return redirect(url_for('notes'))
    
    return render_template('upload_note.html')

@app.route('/download/<type>/<int:id>')
def download_file(type, id):
    if type == 'project':
        project = Project.query.get_or_404(id)
        if project.project_file:
            project.downloads += 1
            db.session.commit()
            return send_from_directory(UPLOAD_FOLDERS['project'], project.project_file, as_attachment=True)
    elif type == 'report':
        project = Project.query.get_or_404(id)
        if project.report_file:
            return send_from_directory(UPLOAD_FOLDERS['report'], project.report_file, as_attachment=True)
    elif type == 'ppt':
        project = Project.query.get_or_404(id)
        if project.ppt_file:
            return send_from_directory(UPLOAD_FOLDERS['ppt'], project.ppt_file, as_attachment=True)
    elif type == 'note':
        note = Note.query.get_or_404(id)
        if note.file_path:
            return send_from_directory(UPLOAD_FOLDERS['note'], note.file_path, as_attachment=True)
    
    flash('File not found!', 'error')
    return redirect(url_for('index'))

@app.route('/verify_project/<int:id>', methods=['POST'])
def verify_project(id):
    project = Project.query.get_or_404(id)
    verification = Verification(
        project_id=id,
        user_name=request.form['user_name'],
        worked=request.form.get('worked') == 'on',
        comment=request.form.get('comment', '')
    )
    db.session.add(verification)
    
    if verification.worked:
        project.verified_count += 1
    
    db.session.commit()
    flash('Thank you for verifying!', 'success')
    return redirect(url_for('project_detail', id=id))

@app.route('/request_project', methods=['GET', 'POST'])
def request_project():
    if request.method == 'POST':
        flash('Request submitted! Seniors will be notified.', 'success')
        return redirect(url_for('projects'))
    return render_template('request_project.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('index'))
    
    projects = Project.query.filter(
        db.or_(
            Project.course_code.ilike(f'%{query}%'),
            Project.subject_name.ilike(f'%{query}%'),
            Project.professor.ilike(f'%{query}%'),
            Project.tech_stack.ilike(f'%{query}%')
        )
    ).limit(10).all()
    
    notes = Note.query.filter(
        db.or_(
            Note.course_code.ilike(f'%{query}%'),
            Note.subject_name.ilike(f'%{query}%'),
            Note.title.ilike(f'%{query}%')
        )
    ).limit(10).all()
    
    return render_template('search.html', query=query, projects=projects, notes=notes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
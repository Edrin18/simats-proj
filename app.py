from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'studyshare-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studyshare.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 10MB for Render free tier

ADMIN_PASSWORD = 'edrin1804081672008'

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
    course_name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    tech_stack = db.Column(db.String(200), nullable=False)
    github_link = db.Column(db.String(500))
    project_file = db.Column(db.String(200))
    report_file = db.Column(db.String(200))
    ppt_file = db.Column(db.String(200))
    demo_video = db.Column(db.String(500))
    uploader_name = db.Column(db.String(100), nullable=False)
    downloads = db.Column(db.Integer, default=0)
    verified_count = db.Column(db.Integer, default=0)
    is_admin_upload = db.Column(db.Boolean, default=False)
    admin_feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    file_path_1 = db.Column(db.String(200))
    file_path_2 = db.Column(db.String(200))
    file_path_3 = db.Column(db.String(200))
    file_path_4 = db.Column(db.String(200))
    file_path_5 = db.Column(db.String(200))
    uploader_name = db.Column(db.String(100), nullable=False)
    rating_count = db.Column(db.Integer, default=0)
    is_admin_upload = db.Column(db.Boolean, default=False)
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
    admin_projects = Project.query.filter_by(is_admin_upload=True).order_by(Project.created_at.desc()).limit(6).all()
    admin_notes = Note.query.filter_by(is_admin_upload=True).order_by(Note.created_at.desc()).limit(6).all()
    user_projects = Project.query.filter_by(is_admin_upload=False).order_by(Project.created_at.desc()).limit(6).all()
    user_notes = Note.query.filter_by(is_admin_upload=False).order_by(Note.created_at.desc()).limit(6).all()
    stats = {
        'total_projects': Project.query.count(),
        'total_notes': Note.query.count()
    }
    return render_template('index.html', admin_projects=admin_projects, admin_notes=admin_notes,
                         user_projects=user_projects, user_notes=user_notes, stats=stats)

@app.route('/projects')
def projects():
    page = request.args.get('page', 1, type=int)
    course_filter = request.args.get('course', '')
    
    query = Project.query.filter_by(is_admin_upload=False)
    
    if course_filter:
        query = query.filter(Project.course_name.ilike(f'%{course_filter}%'))
    
    projects = query.order_by(Project.created_at.desc()).paginate(page=page, per_page=12)
    return render_template('projects.html', projects=projects, course_filter=course_filter)

@app.route('/project/<int:id>')
def project_detail(id):
    project = Project.query.get_or_404(id)
    verifications = Verification.query.filter_by(project_id=id).order_by(Verification.created_at.desc()).limit(5).all()
    return render_template('project_detail.html', project=project, verifications=verifications)

@app.route('/upload_project', methods=['GET', 'POST'])
def upload_project():
    if request.method == 'POST':
        name = request.form['uploader_name']
        
        project_file = request.files.get('project_file')
        report_file = request.files.get('report_file')
        ppt_file = request.files.get('ppt_file')
        
        project_filename = None
        report_filename = None
        ppt_filename = None
        
        if project_file and project_file.filename:
            project_filename = secure_filename(f"{name}_{project_file.filename}")
            project_file.save(os.path.join(UPLOAD_FOLDERS['project'], project_filename))
        
        if report_file and report_file.filename:
            report_filename = secure_filename(f"{name}_{report_file.filename}")
            report_file.save(os.path.join(UPLOAD_FOLDERS['report'], report_filename))
        
        if ppt_file and ppt_file.filename:
            ppt_filename = secure_filename(f"{name}_{ppt_file.filename}")
            ppt_file.save(os.path.join(UPLOAD_FOLDERS['ppt'], ppt_filename))
        
        project = Project(
            course_name=request.form['course_name'],
            description=request.form['description'],
            tech_stack=request.form['tech_stack'],
            github_link=request.form.get('github_link', ''),
            demo_video=request.form.get('demo_video', ''),
            project_file=project_filename,
            report_file=report_filename,
            ppt_file=ppt_filename,
            uploader_name=name,
            is_admin_upload=False
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
    
    query = Note.query.filter_by(is_admin_upload=False)
    if course_filter:
        query = query.filter(Note.course_name.ilike(f'%{course_filter}%'))
    
    notes = query.order_by(Note.created_at.desc()).paginate(page=page, per_page=12)
    return render_template('notes.html', notes=notes, course_filter=course_filter)

@app.route('/upload_note', methods=['GET', 'POST'])
def upload_note():
    if request.method == 'POST':
        name = request.form['uploader_name']
        
        file_1 = request.files.get('note_file_1')
        file_2 = request.files.get('note_file_2')
        file_3 = request.files.get('note_file_3')
        file_4 = request.files.get('note_file_4')
        file_5 = request.files.get('note_file_5')
        
        filename_1 = None
        filename_2 = None
        filename_3 = None
        filename_4 = None
        filename_5 = None
        
        if file_1 and file_1.filename:
            filename_1 = secure_filename(f"{name}_ch1_{file_1.filename}")
            file_1.save(os.path.join(UPLOAD_FOLDERS['note'], filename_1))
        
        if file_2 and file_2.filename:
            filename_2 = secure_filename(f"{name}_ch2_{file_2.filename}")
            file_2.save(os.path.join(UPLOAD_FOLDERS['note'], filename_2))
        
        if file_3 and file_3.filename:
            filename_3 = secure_filename(f"{name}_ch3_{file_3.filename}")
            file_3.save(os.path.join(UPLOAD_FOLDERS['note'], filename_3))
        
        if file_4 and file_4.filename:
            filename_4 = secure_filename(f"{name}_ch4_{file_4.filename}")
            file_4.save(os.path.join(UPLOAD_FOLDERS['note'], filename_4))
        
        if file_5 and file_5.filename:
            filename_5 = secure_filename(f"{name}_ch5_{file_5.filename}")
            file_5.save(os.path.join(UPLOAD_FOLDERS['note'], filename_5))
        
        if not filename_1:
            flash('At least Chapter 1 file is required!', 'error')
            return redirect(url_for('upload_note'))
        
        note = Note(
            course_name=request.form['course_name'],
            title=request.form['title'],
            description=request.form.get('description', ''),
            file_path_1=filename_1,
            file_path_2=filename_2,
            file_path_3=filename_3,
            file_path_4=filename_4,
            file_path_5=filename_5,
            uploader_name=name,
            is_admin_upload=False
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
        chapter = request.args.get('chapter', 1, type=int)
        file_attr = f'file_path_{chapter}'
        filename = getattr(note, file_attr)
        if filename:
            return send_from_directory(UPLOAD_FOLDERS['note'], filename, as_attachment=True)
    
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
            Project.course_name.ilike(f'%{query}%'),
            Project.tech_stack.ilike(f'%{query}%')
        )
    ).limit(10).all()
    
    notes = Note.query.filter(
        db.or_(
            Note.course_name.ilike(f'%{query}%'),
            Note.title.ilike(f'%{query}%')
        )
    ).limit(10).all()
    
    return render_template('search.html', query=query, projects=projects, notes=notes)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['password'] == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Welcome Admin!', 'success')
            return redirect(url_for('admin_panel'))
        else:
            flash('Invalid password!', 'error')
    return render_template('admin_login.html')

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/admin')
def admin_panel():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    projects = Project.query.order_by(Project.created_at.desc()).all()
    notes = Note.query.order_by(Note.created_at.desc()).all()
    return render_template('admin_panel.html', projects=projects, notes=notes)

@app.route('/admin/delete_project/<int:id>')
def admin_delete_project(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/admin/delete_note/<int:id>')
def admin_delete_note(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted successfully!', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/admin/upload_project', methods=['GET', 'POST'])
def admin_upload_project():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        project_file = request.files.get('project_file')
        report_file = request.files.get('report_file')
        ppt_file = request.files.get('ppt_file')
        
        project_filename = None
        report_filename = None
        ppt_filename = None
        
        if project_file and project_file.filename:
            project_filename = secure_filename(f"ADMIN_{project_file.filename}")
            project_file.save(os.path.join(UPLOAD_FOLDERS['project'], project_filename))
        
        if report_file and report_file.filename:
            report_filename = secure_filename(f"ADMIN_{report_file.filename}")
            report_file.save(os.path.join(UPLOAD_FOLDERS['report'], report_filename))
        
        if ppt_file and ppt_file.filename:
            ppt_filename = secure_filename(f"ADMIN_{ppt_file.filename}")
            ppt_file.save(os.path.join(UPLOAD_FOLDERS['ppt'], ppt_filename))
        
        project = Project(
            course_name=request.form['course_name'],
            description=request.form['description'],
            tech_stack=request.form['tech_stack'],
            github_link=request.form.get('github_link', ''),
            demo_video=request.form.get('demo_video', ''),
            project_file=project_filename,
            report_file=report_filename,
            ppt_file=ppt_filename,
            uploader_name='Admin',
            is_admin_upload=True,
            admin_feedback=request.form.get('admin_feedback', '')
        )
        
        db.session.add(project)
        db.session.commit()
        flash('Admin Project uploaded successfully!', 'success')
        return redirect(url_for('admin_panel'))
    
    return render_template('admin_upload_project.html')

@app.route('/admin/upload_note', methods=['GET', 'POST'])
def admin_upload_note():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        file_1 = request.files.get('note_file_1')
        file_2 = request.files.get('note_file_2')
        file_3 = request.files.get('note_file_3')
        file_4 = request.files.get('note_file_4')
        file_5 = request.files.get('note_file_5')
        
        filename_1 = None
        filename_2 = None
        filename_3 = None
        filename_4 = None
        filename_5 = None
        
        if file_1 and file_1.filename:
            filename_1 = secure_filename(f"ADMIN_ch1_{file_1.filename}")
            file_1.save(os.path.join(UPLOAD_FOLDERS['note'], filename_1))
        
        if file_2 and file_2.filename:
            filename_2 = secure_filename(f"ADMIN_ch2_{file_2.filename}")
            file_2.save(os.path.join(UPLOAD_FOLDERS['note'], filename_2))
        
        if file_3 and file_3.filename:
            filename_3 = secure_filename(f"ADMIN_ch3_{file_3.filename}")
            file_3.save(os.path.join(UPLOAD_FOLDERS['note'], filename_3))
        
        if file_4 and file_4.filename:
            filename_4 = secure_filename(f"ADMIN_ch4_{file_4.filename}")
            file_4.save(os.path.join(UPLOAD_FOLDERS['note'], filename_4))
        
        if file_5 and file_5.filename:
            filename_5 = secure_filename(f"ADMIN_ch5_{file_5.filename}")
            file_5.save(os.path.join(UPLOAD_FOLDERS['note'], filename_5))
        
        if not filename_1:
            flash('At least Chapter 1 file is required!', 'error')
            return redirect(url_for('admin_upload_note'))
        
        note = Note(
            course_name=request.form['course_name'],
            title=request.form['title'],
            description=request.form.get('description', ''),
            file_path_1=filename_1,
            file_path_2=filename_2,
            file_path_3=filename_3,
            file_path_4=filename_4,
            file_path_5=filename_5,
            uploader_name='Admin',
            is_admin_upload=True
        )
        
        db.session.add(note)
        db.session.commit()
        flash('Admin Note uploaded successfully!', 'success')
        return redirect(url_for('admin_panel'))
    
    return render_template('admin_upload_note.html')
# Increase upload timeout for Render
@app.errorhandler(413)
def too_large(e):
    flash('File too large. Maximum size is 10MB per file.', 'error')
    return redirect(request.url), 413

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
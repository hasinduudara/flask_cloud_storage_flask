from flask import render_template, url_for, flash, redirect, abort, request
from app import app, db, bcrypt, mail
from app.models import User, File
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import cloudinary.uploader
from sqlalchemy import inspect, text

# Create DB Tables automatically
with app.app_context():
    db.create_all()
    # Ensure missing columns are added for SQLite deployments without migrations
    try:
        inspector = inspect(db.engine)
        columns = {col['name'] for col in inspector.get_columns('file')}
        if 'public_id' not in columns:
            # SQLite supports adding a column; it will be nullable by default
            with db.engine.begin() as conn:
                conn.execute(text('ALTER TABLE file ADD COLUMN public_id VARCHAR(200)'))
    except Exception as e:
        # Non-fatal: log to console; app will still run and surface errors in UI if needed
        print(f"Schema check/migration skipped or failed: {e}")

@app.route("/")
@login_required
def home():
    return redirect(url_for('dashboard'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(username=request.form['username'], email=request.form['email'], password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Check email and password', 'danger')
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file_to_upload = request.files['file']
        if file_to_upload.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if file_to_upload:
            try:
                # Cloudinary "auto" detects image/video/raw
                upload_result = cloudinary.uploader.upload(
                    file_to_upload, 
                    resource_type="auto", 
                    folder="my_flask_app"
                )

                new_file = File(
                    filename=file_to_upload.filename,
                    url=upload_result['secure_url'],
                    public_id=upload_result.get('public_id'),  # ensure we store public_id
                    file_type=upload_result['resource_type'],
                    owner=current_user
                )
                db.session.add(new_file)
                db.session.commit()
                flash('File uploaded successfully!', 'success')
            except Exception as e:
                flash(f'Upload failed: {str(e)}', 'danger')

    files = File.query.filter_by(owner=current_user).all()
    return render_template('dashboard.html', files=files)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user:
            token = user.get_reset_token()
            msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
            # _external=True ensures we get the full http://... link
            link = url_for('reset_token', token=token, _external=True)
            msg.body = f'''To reset your password, visit the following link:
{link}

If you did not make this request then simply ignore this email.
'''
            try:
                mail.send(msg)
                flash('An email has been sent with instructions to reset your password.', 'info')
            except Exception as e:
                print(f"Failed to send email: {str(e)}")
                flash('Failed to send reset email. Please contact support or try again later.', 'danger')
                # For development: show detailed error
                if app.debug:
                    flash(f'Email error: {str(e)}', 'danger')
        else:
            flash('There is no account with that email.', 'warning')
    return render_template('forgot_password.html')

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    if request.method == 'POST':
        hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You can now login', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html')

@app.route("/delete/<int:file_id>", methods=['POST'])
@login_required
def delete_file(file_id):
    file = File.query.get_or_404(file_id)

    # Security Check: Ensure the current user owns this file
    if file.owner != current_user:
        abort(403) # Forbidden

    try:
        # 1. Delete from Cloudinary if we have a public_id
        if getattr(file, 'public_id', None):
            # We must pass the resource_type (image/video/raw) or it might fail
            cloudinary.uploader.destroy(file.public_id, resource_type=file.file_type)

        # 2. Delete from Database
        db.session.delete(file)
        db.session.commit()
        flash('File deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting file: {str(e)}', 'danger')

    return redirect(url_for('dashboard'))
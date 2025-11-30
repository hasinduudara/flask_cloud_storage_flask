from flask import render_template, url_for, flash, redirect, abort, request
from app import app, db, bcrypt, mail
from app.models import User, File
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import cloudinary.uploader
from sqlalchemy import inspect, text
import random
from datetime import datetime, timedelta
from flask import session

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
        login_user(user)
        flash('Account created successfully! Welcome to CloudBox.', 'success')
        return redirect(url_for('dashboard'))
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


@app.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if user:
            # Generate 6-digit OTP
            otp = str(random.randint(100000, 999999))

            # Save OTP and Expiration (Now + 2 minutes) to DB
            user.otp_secret = otp
            user.otp_expiry = datetime.utcnow() + timedelta(minutes=2)
            db.session.commit()

            # Send Email
            msg = Message('Password Reset OTP', sender='noreply@demo.com', recipients=[user.email])
            msg.body = f'''Your OTP for password reset is: {otp} This code expires in 2 minutes.
            If you did not request this, please ignore this email.
            '''
            try:
                mail.send(msg)
                # Store email in session to use in next step
                session['reset_email'] = email
                flash('OTP sent to your email. It expires in 2 minutes.', 'info')
                return redirect(url_for('verify_otp'))
            except Exception as e:
                flash('Error sending email. Try again.', 'danger')
        else:
            flash('No account found with that email.', 'warning')

    return render_template('forgot_password.html')


# 2. PAGE TO ENTER OTP
@app.route("/verify_otp", methods=['GET', 'POST'])
def verify_otp():
    if 'reset_email' not in session:
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        otp_input = request.form['otp']
        email = session['reset_email']
        user = User.query.filter_by(email=email).first()

        if user:
            # Check 1: Is OTP correct?
            if user.otp_secret != otp_input:
                flash('Invalid OTP. Please try again.', 'danger')
            # Check 2: Is OTP expired?
            elif user.otp_expiry < datetime.utcnow():
                flash('OTP has expired. Please request a new one.', 'warning')
                return redirect(url_for('forgot_password'))
            else:
                # Success! Allow password reset
                session['otp_verified'] = True
                return redirect(url_for('reset_new_password'))
        else:
            flash('User not found.', 'danger')

    return render_template('verify_otp.html')


# 3. PAGE TO SET NEW PASSWORD
@app.route("/reset_new_password", methods=['GET', 'POST'])
def reset_new_password():
    # Security: Make sure they actually verified the OTP
    if 'otp_verified' not in session or not session['otp_verified']:
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        password = request.form['password']
        email = session['reset_email']
        user = User.query.filter_by(email=email).first()

        if user:
            # Hash new password
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user.password = hashed_password

            # Clear OTP fields for security
            user.otp_secret = None
            user.otp_expiry = None
            db.session.commit()

            # Clear session
            session.pop('reset_email', None)
            session.pop('otp_verified', None)

            flash('Your password has been updated! You can now login.', 'success')
            return redirect(url_for('login'))

    return render_template('reset_token.html')  # Reusing your existing template

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
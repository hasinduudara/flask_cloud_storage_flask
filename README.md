# ☁️ CloudBox - Personal Cloud Storage

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Flask-2.0+-green.svg" alt="Flask">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

CloudBox is a secure, lightweight cloud storage application built with Python (Flask). It allows users to register, upload, manage, and preview files (Images, Videos, PDFs, Docs) in the cloud using the Cloudinary API. It features a modern, responsive UI built with Tailwind CSS and includes a secure OTP-based password reset system.

## ✨ Features

### 🔐 Secure Authentication
- User registration and login system with hashed passwords (Bcrypt)
- Session management with Flask-Login
- Secure OTP-based password reset flow

### ☁️ Cloud Storage
- Seamless integration with Cloudinary for storing images, videos, and raw documents
- Automatic file type detection and categorization
- Efficient cloud resource management

### 📂 File Management
- **Drag-and-drop upload support** for seamless file uploads
- **Auto-detection of file types** (images, videos, documents)
- **Instant Previews** for Images and Videos
- **Smart icons** for PDFs, Word Docs, and Text files
- **Secure Delete** functionality (removes from both Database & Cloud)
- Grid-based dashboard for easy file browsing

### 🔑 Forgot Password Flow
- Secure 6-digit OTP (One-Time Password) verification
- 2-minute expiration time for enhanced security
- Email delivery via SMTP (Mailtrap for testing, Gmail for production)

### 🎨 Modern UI
- Fully responsive interface using Tailwind CSS
- Glassmorphism effects for modern aesthetics
- Toast notifications for user feedback
- Clean, intuitive design

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3, Flask |
| **Database** | SQLite (SQLAlchemy ORM) |
| **Frontend** | HTML5, Jinja2 Templates, Tailwind CSS (via CDN) |
| **Cloud Service** | Cloudinary API (Free Tier) |
| **Email Service** | Mailtrap (SMTP for testing) / Gmail (Production) |
| **Libraries** | Flask-Login, Flask-Mail, Flask-Bcrypt, python-dotenv |

## 🚀 Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/hasinduudara/flask_cloud_storage_flask.git
cd cloudbox
```

### 2. Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a file named `.env` in the root directory and add your API keys. You will need free accounts from [Cloudinary](https://cloudinary.com/) and [Mailtrap](https://mailtrap.io/).

**.env file content:**

```env
# Flask Config
SECRET_KEY=your_random_secret_string_here
SQLALCHEMY_DATABASE_URI=sqlite:///storage.db

# Cloudinary Config (Get these from your Dashboard)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Email Config (Mailtrap Sandbox or Gmail)
MAIL_SERVER=sandbox.smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USERNAME=your_mailtrap_username
MAIL_PASSWORD=your_mailtrap_password
MAIL_USE_TLS=True
MAIL_USE_SSL=False
```

### 5. Run the Application

```bash
python run.py
```

The application will start at **http://127.0.0.1:5000/**

## 📸 Screenshots

### Dashboard
Manage your files with a clean, grid-based layout.

### File Preview
Instant previews for uploaded images and videos before submitting.

### OTP Verification
Secure 2-minute expiration OTP code for password resets.

## 📂 Project Structure

```
flask_cloud_storage/
├── .env                 # API Keys (Not included in repo)
├── requirements.txt     # Python Dependencies
├── run.py               # Entry Point
└── app/
    ├── __init__.py      # App Config
    ├── models.py        # Database Models (User, File)
    ├── routes.py        # Application Logic
    └── templates/       # HTML Files
        ├── base.html    # Main Layout (Tailwind)
        ├── dashboard.html
        ├── login.html
        ├── register.html
        ├── forgot_password.html
        ├── verify_otp.html
        └── reset_token.html
```

## 🔧 Configuration

### Cloudinary Setup
1. Sign up for a free account at [Cloudinary](https://cloudinary.com/)
2. Navigate to your Dashboard
3. Copy your Cloud Name, API Key, and API Secret
4. Add them to your `.env` file

### Email Setup (Mailtrap)
1. Sign up for a free account at [Mailtrap](https://mailtrap.io/)
2. Create a new inbox
3. Copy the SMTP credentials
4. Add them to your `.env` file

### Email Setup (Gmail - Production)
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password
3. Update your `.env` file:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_USE_TLS=True
MAIL_USE_SSL=False
```

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Future Enhancements

- [ ] File sharing with public links
- [ ] Folder organization
- [ ] File search functionality
- [ ] Storage usage analytics
- [ ] Multi-user file collaboration
- [ ] Dark mode toggle

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📧 Contact

**Hasindu Udara**

- GitHub: [@hasinduudara](https://github.com/hasinduudara)
- Project Link: [https://github.com/hasinduudara/flask_cloud_storage_flask](https://github.com/hasinduudara/flask_cloud_storage_flask)

---

<p align="center">
  Built with ❤️ by Hasindu Udara
</p>

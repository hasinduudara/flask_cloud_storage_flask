☁️ CloudBox - Personal Cloud Storage

CloudBox is a secure, lightweight cloud storage application built with Python (Flask). It allows users to register, upload, manage, and preview files (Images, Videos, PDFs, Docs) in the cloud using the Cloudinary API. It features a modern, responsive UI built with Tailwind CSS and includes a secure OTP-based password reset system.

✨ Features

🔐 Secure Authentication: User registration and login system with hashed passwords (Bcrypt).

☁️ Cloud Storage: Seamless integration with Cloudinary for storing images, videos, and raw documents.

📂 File Management:

Drag-and-drop upload support.

Auto-detection of file types.

Instant Previews for Images and Videos.

Smart icons for PDFs, Word Docs, and Text files.

Secure "Delete" functionality (removes from Database & Cloud).

🔑 Forgot Password Flow: Secure 6-digit OTP (One-Time Password) verification sent via Email (SMTP).

🎨 Modern UI: Fully responsive interface using Tailwind CSS with glassmorphism effects and toast notifications.

🛠️ Tech Stack

Backend: Python 3, Flask

Database: SQLite (SQLAlchemy)

Frontend: HTML5, Jinja2 Templates, Tailwind CSS (via CDN)

Cloud Service: Cloudinary API (Free Tier)

Email Service: Mailtrap (SMTP for testing) / Gmail (Production)

Libraries: Flask-Login, Flask-Mail, Flask-Bcrypt, python-dotenv

🚀 Installation & Setup

Follow these steps to run the project locally.

1. Clone the Repository

git clone [https://github.com/hasinduudara/cloudbox.git](https://github.com/hasinduudara/flask_cloud_storage_flask.git)
cd cloudbox


2. Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate


3. Install Dependencies

pip install -r requirements.txt


4. Configure Environment Variables

Create a file named .env in the root directory and add your API keys. You will need free accounts from Cloudinary and Mailtrap.

.env file content:

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


5. Run the Application

python run.py


The application will start at http://127.0.0.1:5000/.

📸 Screenshots

Dashboard

Manage your files with a clean, grid-based layout.

File Preview

Instant previews for uploaded images and videos before submitting.

OTP Verification

Secure 2-minute expiration OTP code for password resets.

📂 Project Structure

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


🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements.

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 License

Distributed under the MIT License. See LICENSE for more information.

<p align="center">
Built with ❤️ by Hasindu Udara
</p>
from flask import Flask, request
import os
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from groq import Groq
from dotenv import load_dotenv
import json
from Services.UserService import create_user
from Services.DocumentService import grade_resume, getAllResumeEntries
from flask_dance.contrib.google import make_google_blueprint, google

# Initialize Flask app
app = Flask(__name__)
CORS(app)
# db = SQLAlchemy(app)
load_dotenv()

# Load environment variables
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = 'Uploads'
ALLOWED_EXTENSIONS = {'.txt', '.pdf', '.docx'}

# Google OAuth setup
app.config["GOOGLE_OAUTH_CLIENT_ID"] = os.getenv("OAUTH_CLIENT_ID")
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = os.getenv("OAUTH_SECRET")

google_bp = make_google_blueprint(
    client_id=app.config["GOOGLE_OAUTH_CLIENT_ID"],
    client_secret=app.config["GOOGLE_OAUTH_CLIENT_SECRET"],
    scope=["profile", "email"],
    redirect_url="/login/google/authorized"
)
app.register_blueprint(google_bp, url_prefix="/login")

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and os.path.splitext(filename)[-1].lower() in ALLOWED_EXTENSIONS

# API endpoint to handle grading requests
@app.route('/api/grade', methods=['POST'])
def grade():
    # Handle file uploads and processing
    entry_title = request.form.get('title')
    resume_file = request.files.get('resume')
    job_file = request.files.get('job_description')

    if not resume_file or not job_file:
        return "Missing files", 400

    if not allowed_file(resume_file.filename) or not allowed_file(job_file.filename):
        return "Invalid file format", 400

    # Ensure upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Save uploaded files
    resume_file.save(os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename))
    job_file.save(os.path.join(app.config['UPLOAD_FOLDER'], job_file.filename))

    # read binary files form the request body
    # Grade the resume against the job description
    grade, feedback = grade_resume(os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename), 
                                   os.path.join(app.config['UPLOAD_FOLDER'], job_file.filename), 
                                   entry_title)

    return json.dumps({"grade": grade, "feedback": feedback}), 200

# API endpoint to get all resume entries
@app.route('/api/allResumeEntries', methods=['GET'])
def get_all_resume_entries():
    # Logic to retrieve all resume entries from the database
    data = getAllResumeEntries()
    if(data is None):
        return json.dumps({"status": "error", "message": "Could not fetch resume entries"}), 500
    
    return json.dumps({"status": "success", "data": data}), 200


@app.route('/signup', methods=['POST'])
def signup():
    if not google.authorized:
        return {"status": "error", "message": "Not authenticated"}, 401
    
    try:
        # Get user info from Google
        google_user = google.get("/oauth2/v2/userinfo").json()
        
        # Create user data dictionary
        user_data = {
            'email': google_user['email'],
            'name': google_user['name'],
            'google_id': google_user['id'],
        }
        
        # Create user using UserService
        result = create_user(user_data)
        if not result:
            return {"status": "error", "message": "User creation failed"}, 400
            
        return {"status": "success", "user": result}, 200
        
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

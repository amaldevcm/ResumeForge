from flask import Flask, request, session
import os
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import json
from Services.UserService import (
    create_user, get_current_user, get_user_by_id, login_user, signup_user,
    update_user, change_password, delete_user, logout_user, user_to_dict
)
from Services.DocumentService import getBestResumes, saveDocument
from Services.DocumentService import getDocumentById, grade_resume, getAllResumes
from Services.JobService import get_job_details, get_jobs, allJobs, getJobById
from flask_dance.contrib.google import make_google_blueprint, google

# Initialize Flask app
app = Flask(__name__)
load_dotenv()

app.secret_key = os.getenv("FLASK_SECRET_KEY")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
CORS(app, supports_credentials=True, origins=[FRONTEND_ORIGIN])
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Load environment variables
app.config["TEMPLATES_AUTO_RELOAD"] = True
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



# API Routes
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
@app.route('/api/resumeEntries', methods=['GET'])
def get_all_resume_entries():
    # get id from request parameters
    id = request.args.get('id')
    print('id=',id)
    if not id:
        data = getAllResumes()
    else:
        data = getDocumentById(id)
    if(data is None):
        return json.dumps({"status": "error", "message": "Could not fetch resume entries"}), 500
    
    return json.dumps({"status": "success", "data": data}), 200

# API endpoint to handle new document uploads
@app.route('/api/newDocument', methods=['POST'])
def new_document():
    entry_title = request.form.get('title')
    resume_file = request.files.get('resume')

    if not resume_file:
        return "Missing files", 400

    if not allowed_file(resume_file.filename):
        return "Invalid file format", 400

    # Ensure upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Save uploaded files
    resume_file.save(os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename))
    saveDocument(os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename), entry_title)
    return json.dumps({"status": "success", "message": "File uploaded successfully"}), 200

# API endpoint for Google OAuth signup/login
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

# API endpoint for email/password signup
@app.route('/api/signup', methods=['POST'])
def api_signup():
    data = request.get_json() or {}
    try:
        new_user = signup_user(data)
        session['user_id'] = str(new_user.id)
        return json.dumps({"status": "success", "user": user_to_dict(new_user)}), 201
    except ValueError as e:
        return json.dumps({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}), 500

# API endpoint for email/password login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    try:
        user = login_user(data.get('email'), password=data.get('password'))
        session['user_id'] = str(user.id)
        return json.dumps({"status": "success", "user": user_to_dict(user)}), 200
    except ValueError as e:
        return json.dumps({"status": "error", "message": str(e)}), 401
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}), 500

# API endpoint to log the current user out
@app.route('/api/logout', methods=['POST'])
def logout():
    logout_user()
    return json.dumps({"status": "success", "message": "Logged out"}), 200

# API endpoint to fetch the logged-in user's profile
@app.route('/api/currentUser', methods=['GET'])
def current_user():
    try:
        user = get_current_user()
        return json.dumps({"status": "success", "user": user}), 200
    except ValueError as e:
        return json.dumps({"status": "error", "message": str(e)}), 401
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}), 500

# API endpoint to update the logged-in user's profile
@app.route('/api/updateProfile', methods=['PUT'])
def update_profile():
    user_id = session.get('user_id')
    if not user_id:
        return json.dumps({"status": "error", "message": "Not authenticated"}), 401

    try:
        data = request.get_json() or {}
        allowed = {k: v for k, v in data.items() if k in ('first_name', 'last_name', 'email')}
        updated = update_user(user_id, allowed)
        return json.dumps({"status": "success", "user": user_to_dict(updated)}), 200
    except ValueError as e:
        return json.dumps({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}), 500

# API endpoint to change the logged-in user's password
@app.route('/api/changePassword', methods=['POST'])
def change_password_route():
    user_id = session.get('user_id')
    if not user_id:
        return json.dumps({"status": "error", "message": "Not authenticated"}), 401

    try:
        data = request.get_json() or {}
        change_password(user_id, data.get('current_password'), data.get('new_password'))
        return json.dumps({"status": "success", "message": "Password updated"}), 200
    except ValueError as e:
        return json.dumps({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}), 500

# API endpoint to delete the logged-in user's account
@app.route('/api/deleteAccount', methods=['DELETE'])
def delete_account():
    user_id = session.get('user_id')
    if not user_id:
        return json.dumps({"status": "error", "message": "Not authenticated"}), 401

    try:
        # NOTE: does not cascade-delete the user's Document rows / Pinecone vectors / Supabase files — follow-up item.
        delete_user(user_id)
        logout_user()
        return json.dumps({"status": "success", "message": "Account deleted"}), 200
    except ValueError as e:
        return json.dumps({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}), 500

# API endpoint to handle job search requests
@app.route('/api/jobs', methods=['GET'])
def jobs():
    jobTitle = request.args.get('query')
    location = request.args.get('location')
    if not jobTitle or not location:
        return "Missing query or location parameters", 400
    
    try:
        job_results = get_jobs(jobTitle, location)
        return json.dumps({"status": "success", "jobs": job_results}), 200
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}), 500

# API endpoint to fetch job details based on a provided URL
@app.route('/api/jobDetails', methods=['GET'])
def job_details(): 
    url = request.args.get('url')
    if not url:
        return "Missing url parameter", 400
    
    try:
        details = get_job_details(url)
        if details is None:
            return json.dumps({"status": "error", "message": "Job not found"}), 404
        return json.dumps({"status": "success", "details": details}), 200
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}), 500
    
# API endpoint to fetch the best matching resumes for a given job description
@app.route('/api/bestResume', methods=['GET'])
def best_resume():
    job_id = request.args.get('job_id')
    job = getJobById(job_id)
    # print(job_id, job)

    if not job:
        return "Missing job_description parameter", 400
    
    try:

        best_resumes = getBestResumes(jd_text=job['description'], top_k=3)
        if not best_resumes:
            return json.dumps({"status": "error", "message": "No resumes found"}), 404
        return json.dumps({"status": "success", "resumes": best_resumes}), 200
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}), 500
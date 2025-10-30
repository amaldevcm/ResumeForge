from flask import Flask, render_template, request, redirect
import os
import pdfplumber
import docx
from groq import Groq
from dotenv import load_dotenv
import json
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import io
import base64
import pinecone

# Initialize Flask app
app = Flask(__name__)
load_dotenv()
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'.txt', '.pdf', '.docx'}
resume_file_name = ""
job_file_name = ""

    
# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and os.path.splitext(filename)[-1].lower() in ALLOWED_EXTENSIONS

# API endpoint to handle grading requests
@app.route('/api/grade', methods=['POST'])
def grade():
    # Handle file uploads and processing
    resume_file = request.files.get('resume')
    job_file = request.files.get('job_description')

    if not resume_file or not job_file:
        return "Missing files", 400

    if not allowed_file(resume_file.filename) or not allowed_file(job_file.filename):
        return "Invalid file format", 400
    
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    resume_file.save(os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename))
    job_file.save(os.path.join(app.config['UPLOAD_FOLDER'], job_file.filename))

    global resume_file_name
    global job_file_name

    return json.dumps({"grade": grade, "feedback": "Good match!"})
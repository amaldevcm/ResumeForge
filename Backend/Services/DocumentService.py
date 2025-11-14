import uuid
from datetime import datetime
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from Prompts.ResumeReview import get_improvement_suggestions
from Services.UserService import get_current_user
from Models.Models import Resume, Document
from Services.PineconeService import save_vector
from DB import SessionLocal
import pdfplumber
import docx
import re
import os


# Function to load files
def load_file(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    elif ext == '.pdf':
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    
    elif ext == '.docx':
        doc = docx.Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    else:
        raise ValueError(f"Unsupported file format: {ext}. Use .txt, .pdf, or .docx")

# Function to truncate text to a maximum number of words
def truncate_text(text, max_words=512):
    return ' '.join(text.split()[:max_words])

# Create vector embeddings and store them
def create_embeddings(resume_text, job_text):

    # Sentence Transformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Create embeddings
    resume_embedding = model.encode(resume_text, convert_to_tensor=False)
    job_embedding = model.encode(job_text, convert_to_tensor=False) 

    # Section-wise encoding of the resume
    # Split resume into sections by common headings (e.g., Experience, Education, Skills)
    section_pattern = re.compile(r'(?i)(experience|education|skills|projects|summary|certifications|achievements|contact)[\s:\n]+')
    sections = section_pattern.split(resume_text)
    section_dict = {}

    # sections alternates between content and headings
    for i in range(1, len(sections), 2):
        heading = sections[i].strip().capitalize()
        content = sections[i+1].strip()
        section_dict[heading] = content

    # Encode each section separately
    section_embeddings = {}
    for heading, content in section_dict.items():
        section_embeddings[heading] = model.encode(content, convert_to_tensor=False)

    # Calculate similarity score
    similarity = cosine_similarity(
        resume_embedding.reshape(1, -1), 
        job_embedding.reshape(1, -1)
    )[0][0]

    # Store embeddings in memory (you can later use a vector database)
    vector_store = {
        'resume': resume_embedding,
        'job': job_embedding,
        'section_embeddings': section_embeddings,
        'similarity': similarity
    }
    return vector_store

# Function to grade resume against job description
def grade_resume(resume, jobDesc, title):
    # Convert binary files to text
    resume = load_file(resume)
    jobDesc = load_file(jobDesc)

    # Create embeddings
    vector_store = create_embeddings(truncate_text(resume), truncate_text(jobDesc))
    resume_index = save_vector(vector_store['resume']) 
    job_index = save_vector(vector_store['job'])

    # Save resume and job embeddings to Pinecone
    try:
        db = SessionLocal()
        new_resume = Resume(
            id = str(uuid.uuid4()),
            user_id = get_current_user()['id'],
            resume_text = resume,
            resume_vector_id = resume_index,
            created_date = datetime.now().isoformat(),
            updated_date = datetime.now().isoformat()
        )

        new_document = Document(
            id = str(uuid.uuid4()),
            user_id = get_current_user()['id'],
            title = title,
            resume_id = new_resume.id,
            jd_text = jobDesc,
            jd_vector_id = job_index,
            created_date = datetime.now().isoformat(),
            updated_date = datetime.now().isoformat()
        )
        db.add(new_resume)
        db.add(new_document)
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Error saving document: {str(e)}")
    finally:
        db.close()
    

    # Convert similarity score to grade (0-100)
    grade = int(vector_store['similarity'] * 100)
    feedback = get_improvement_suggestions(resume, jobDesc)
    return grade, feedback

def getAllResumeEntries():
    try:
        db = SessionLocal()
        # Retrieve all resume entries for a user
        uid = get_current_user()['id']
        documents = db.query(Document).filter(Document.user_id == uid).all()
        result = []
        for document in documents:
            resume = db.query(Resume).filter(Resume.id == document.resume_id).first()
            result.append({
                "id": str(document.id),
                "title": document.title,
                "resume_text": resume.resume_text if resume else None,
                "job_description": document.jd_text,
                "created_date": document.created_date,
                "updated_date": document.updated_date
            })
        return result
    except Exception as e:
        raise Exception(f"Error retrieving resumes: {str(e)}")
    finally:
        db.close()

def get_resume_by_id(resume_id):
    try:
        db = SessionLocal()
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if resume is None:
            return None
        return {
            "id": str(resume.id),
            "resume_text": resume.resume_text,
            "job_description": resume.jd_text,
            "created_date": resume.created_date,
            "updated_date": resume.updated_date
        }
    except Exception as e:
        raise Exception(f"Error retrieving resume: {str(e)}")
    finally:
        db.close()



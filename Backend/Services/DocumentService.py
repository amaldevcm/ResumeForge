from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re
import os
from Services.PineconeService import save_vector
import pdfplumber
import docx


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


def grade_resume(resume_path, job_path):
    resume = load_file(resume_path)
    jobDesc = load_file(job_path)

    vector_store = create_embeddings(truncate_text(resume), truncate_text(jobDesc))
    index = save_to_pinecone(vector_store)
    # Convert similarity score to grade (0-100)
    grade = int(vector_store['similarity'] * 100)
    return grade, vector_store
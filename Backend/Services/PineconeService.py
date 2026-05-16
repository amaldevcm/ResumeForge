import os
from pinecone import Pinecone, ServerlessSpec
import uuid
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from Services.UserService import get_current_user

load_dotenv()
# Function to initialize Pinecone
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)

# Index name for storing resume embeddings
index_name = os.getenv("PINECONE_INDEX_NAME")
host_name = os.getenv("PINECONE_HOST")

# Function to save vector embedding to Pinecone
def save_vector(embedding, vector_id=None, metadata=None):
    global index_name, pc, host_name

    dimension = len(embedding)
    existing = [idx.name for idx in pc.list_indexes()]

    if index_name not in existing:
        pc.create_index(
            index_name,
            dimension=dimension,
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )

    index = pc.Index(host=host_name)

    if vector_id is None:
        vector_id = str(uuid.uuid4())

    index.upsert(vectors=[{
        "id": vector_id,
        "values": embedding,
        "metadata": metadata
    }])

    return vector_id

# Function to fetch vector by ID
def fetch_vector(vector_id):
    global index_name, pc
    
    index_names = [idx.name for idx in pc.list_indexes()]
    if index_name not in index_names:
        raise ValueError(f"Index {index_name} does not exist")

    index = pc.Index(index_name)
    result = index.fetch(ids=[vector_id])

    if vector_id in result['vectors']:
        return result['vectors'][vector_id]
    else:
        return None
    
# Function to delete vector by ID
def delete_vector(vector_id):
    global index_name, pc
    
    index_names = [idx.name for idx in pc.list_indexes()]
    if index_name not in index_names:
        raise ValueError(f"Index {index_name} does not exist")

    index = pc.Index(index_name)
    index.delete(ids=[vector_id])

# Function to update vector embedding
def update_vector(vector_id, new_embedding, new_metadata=None):
    global index_name, pc
    
    index_names = [idx.name for idx in pc.list_indexes()]
    if index_name not in index_names:
        raise ValueError(f"Index {index_name} does not exist")

    index = pc.Index(index_name)
    record = (vector_id, new_embedding, new_metadata) if new_metadata is not None else (vector_id, new_embedding)
    index.upsert([record])
    return vector_id


# Function to find best resumes for a JD using cosine similarity
def findBestResumes(jd_text, top_k=3):
    global index_name, pc, host_name

    try:
        existing = [idx.name for idx in pc.list_indexes()]
        if index_name not in existing:
            raise ValueError(f"Index {index_name} does not exist")

        index = pc.Index(host=host_name)
        model = SentenceTransformer('all-MiniLM-L6-v2')

        user_id = str(get_current_user()['id'])
        jd_embedding = model.encode(jd_text, convert_to_tensor=False).tolist()
        
        results = index.query(
            vector=jd_embedding,
            top_k=int(top_k),
            filter={"user_id": user_id},
            include_metadata=True
        )
        
        resume_data = [
            {
                "resume_id": match["metadata"]["resume_id"],
                "score": round(match["score"], 4)
            }
            for match in results["matches"]
        ]


    except Exception as e:
        resume_data = []
        print(f"extraction error: {e}")

    return resume_data
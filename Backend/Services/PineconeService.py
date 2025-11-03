import os
from pinecone import Pinecone
import uuid
from dotenv import load_dotenv

load_dotenv()
# Function to initialize Pinecone
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key, environment='us-west1-gcp')

index_name = "resume-forge"
if not pc.has_index(index_name):
    pc.create_index_for_model(
        name=index_name,
        cloud="aws",
        region="us-east-1",
        embed={
            "model":"llama-text-embed-v2",
            "field_map":{"text": "chunk_text"}
        }
    )

# Function to save vector embedding to Pinecone
def save_vector(embedding, index_name='resume-forge', vector_id=None, metadata=None):
    if not isinstance(embedding, (list, tuple)):
        raise TypeError("embedding must be a list or tuple of floats")
    dimension = len(embedding)

    if index_name not in pc.list_indexes():
        pc.create_index(index_name, dimension=dimension)
    index = pc.Index(index_name)

    if vector_id is None:
        vector_id = str(uuid.uuid4())

    # upsert expects (id, vector) or (id, vector, metadata)
    record = (vector_id, embedding, metadata) if metadata is not None else (vector_id, embedding)
    index.upsert([record])
    return vector_id

# Function to fetch vector by ID
def fetch_vector(vector_id, index_name='resume-forge'):
    if index_name not in pc.list_indexes():
        raise ValueError(f"Index {index_name} does not exist")

    index = pc.Index(index_name)
    result = index.fetch(ids=[vector_id])

    if vector_id in result['vectors']:
        return result['vectors'][vector_id]
    else:
        return None
    
# Function to delete vector by ID
def delete_vector(vector_id, index_name='resume-forge'):
    if index_name not in pc.list_indexes():
        raise ValueError(f"Index {index_name} does not exist")

    index = pc.Index(index_name)
    index.delete(ids=[vector_id])

# Function to update vector embedding
def update_vector(vector_id, new_embedding, index_name='resume-forge', new_metadata=None):
    if index_name not in pc.list_indexes():
        raise ValueError(f"Index {index_name} does not exist")

    index = pc.Index(index_name)
    record = (vector_id, new_embedding, new_metadata) if new_metadata is not None else (vector_id, new_embedding)
    index.upsert([record])
    return vector_id
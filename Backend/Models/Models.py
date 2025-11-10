from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String
from DB import Base
import uuid
    
class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True, unique=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    created_date = Column(String)
    updated_date = Column(String)
    oauth_provider = Column(String, nullable=True)
    oauth_id = Column(String, nullable=True)
    password = Column(String)


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID, primary_key=True, index=True, unique=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(UUID, index=True)
    title = Column(String, index=True)
    resume_id = Column(String)
    jd_text = Column(String)
    jd_vector_id = Column(String)
    created_date = Column(String)
    updated_date = Column(String)


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(UUID, primary_key=True, index=True, unique=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(UUID, index=True)
    resume_text = Column(String)
    resume_vector_id = Column(String)
    created_date = Column(String)
    updated_date = Column(String)

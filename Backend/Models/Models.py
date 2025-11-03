from sqlalchemy import Column, Integer, String
from DB import Base
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
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

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    title = Column(String, index=True)
    resume_vector = Column(String)
    jd_text = Column(String)
    jd_vector = Column(String)
    created_date = Column(String)
    updated_date = Column(String)


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    resume_text = Column(String)
    resume_vector = Column(String)
    created_date = Column(String)
    updated_date = Column(String)

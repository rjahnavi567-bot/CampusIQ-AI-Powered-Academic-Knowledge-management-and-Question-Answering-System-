from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from app.database.connection import Base
from datetime import datetime
from sqlalchemy import Boolean
from datetime import datetime
class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True)

    document_id = Column(Integer)

    topic = Column(String)

    keywords = Column(String)

    source_file = Column(String)

    file_type = Column(String)

    chunk_text = Column(String)
    page_no = Column(Integer)
    similarity_score = Column(String)



class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String)
    subject = Column(String)

    file_path = Column(String)

    unit = Column(String)
    primary_subject = Column(String)
    secondary_subjects = Column(Text)
    subject_confidence = Column(Float)
    

    subject_detected_by = Column(String)

    uploaded_by = Column(Integer)

    status = Column(String)

    chunk_count = Column(Integer)
    file_hash = Column(String, nullable=True)

    content_signature = Column(Text, nullable=True)

    embedding = Column(Text, nullable=True)
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    parent_subject = Column(String)

    matched_keywords = Column(Text)

    subject_detection_method = Column(String)
class Subject(Base):

    __tablename__ = "subjects"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        unique=True,
        nullable=False
    )

    description = Column(
        Text,
        nullable=False
    )

    embedding = Column(
        Text,
        nullable=True
    )
class QuestionHistory(Base):

    __tablename__ = "question_history"

    id = Column(
        Integer,
        primary_key=True
    )

    question = Column(Text)

    answer = Column(Text)

    document_name = Column(String)

    
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class DocumentImage(Base):

    __tablename__ = "document_images"

    id = Column(
        Integer,
        primary_key=True
    )

    document_id = Column(
        Integer
    )

    image_path = Column(
        String
    )

    page_no = Column(
        Integer
    )

    caption = Column(
        Text
    )

    # NEW

    title = Column(
        String
    )

    image_hash = Column(
        String,
        unique=True
    )

    source_file = Column(
        String
    )
    category = Column(String(100))

    classification_confidence = Column(Float)
    confidence_score = Column(Integer)
class AcademicSubject(Base):

    __tablename__ = "academic_subjects"

    id = Column(Integer, primary_key=True)

    subject_name = Column(String, nullable=False)

    parent_subject = Column(String)

    branch = Column(String)

    description = Column(Text)

    keywords = Column(Text)

    topics = Column(Text)

    aliases = Column(Text)

    embedding = Column(Text)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    email = Column(String, unique=True)

    password = Column(String)

    role = Column(String)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
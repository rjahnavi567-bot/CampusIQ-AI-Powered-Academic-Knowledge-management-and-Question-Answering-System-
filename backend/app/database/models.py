from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime
)
from app.database.connection import Base
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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    role = Column(String)

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String)

    file_path = Column(String)

    subject = Column(String)

    unit = Column(String)

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
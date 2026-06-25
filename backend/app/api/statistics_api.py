from fastapi import APIRouter
from app.database.connection import SessionLocal
from app.database.models import Document, Chunk, User
from app.services.chroma_service import collection
from sqlalchemy import func
from app.database.models import QuestionHistory
router = APIRouter()
@router.get("/statistics")
def get_statistics():


    file_types = db.query(
    Chunk.file_type,
    func.count(Chunk.id)
).group_by(
    Chunk.file_type
).all()
    
    file_type_stats = {
    file_type: count
    for file_type, count in file_types
}

    db = SessionLocal()
    db.query(
    Chunk.file_type,
    func.count(Chunk.id)
).group_by(Chunk.file_type).all()
    question_count = db.query(
    QuestionHistory).count()
    try:

        return {
    "documents": db.query(Document).count(),
    "chunks": db.query(Chunk).count(),
    "users": db.query(User).count(),
    "questions_asked": question_count,
    "chroma_records": collection.count()
}
        
    finally:
        db.close()
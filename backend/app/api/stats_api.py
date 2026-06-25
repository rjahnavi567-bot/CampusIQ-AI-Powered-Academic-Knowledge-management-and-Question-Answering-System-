from fastapi import APIRouter
from app.database.connection import SessionLocal
from app.database.models import (
    Document,
    Chunk,
    QuestionHistory
)

router = APIRouter()

@router.get("/stats")
def get_stats():

    db = SessionLocal()

    try:

        document_count = db.query(
            Document
        ).count()

        chunk_count = db.query(
            Chunk
        ).count()

        question_count = db.query(
            QuestionHistory
        ).count()

        return {
            "documents": document_count,
            "chunks": chunk_count,
            "questions": question_count,
            "sources": document_count
        }

    finally:
        db.close()
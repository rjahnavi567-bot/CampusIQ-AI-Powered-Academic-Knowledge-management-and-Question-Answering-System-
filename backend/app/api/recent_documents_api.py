from fastapi import APIRouter
from app.database.connection import SessionLocal
from app.database.models import Document

router = APIRouter()

@router.get("/recent-documents")
def recent_documents():

    db = SessionLocal()

    try:

        documents = (
            db.query(Document)
            .order_by(Document.created_at.desc())
            .limit(10)
            .all()
        )

        return documents

    finally:
        db.close()
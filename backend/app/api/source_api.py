from fastapi import APIRouter
from app.database.connection import SessionLocal
from app.database.models import Document

router = APIRouter()
@router.get("/sources")
def get_sources():

    db = SessionLocal()

    try:

        docs = db.query(Document).all()

        result = []

        for doc in docs:

            result.append({
                "id": doc.id,
                "filename": doc.filename,
                "subject": doc.subject,
                "unit": doc.unit
            })

        return result

    finally:
        db.close()
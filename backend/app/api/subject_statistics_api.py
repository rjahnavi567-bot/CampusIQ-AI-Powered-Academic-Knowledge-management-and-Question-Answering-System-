from fastapi import APIRouter
from sqlalchemy import func

from app.database.connection import SessionLocal
from app.database.models import Document

router = APIRouter()

@router.get("/statistics/subjects")
def subject_statistics():

    db = SessionLocal()

    try:

        results = (
            db.query(
                Document.subject,
                func.count(
                    Document.id
                ).label("count")
            )
            .group_by(
                Document.subject
            )
            .all()
        )

        return [
            {
                "subject": row[0],
                "documents": row[1]
            }
            for row in results
        ]

    finally:
        db.close()
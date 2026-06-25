from fastapi import APIRouter
from sqlalchemy import func

from app.database.connection import SessionLocal
from app.database.models import (
    Document,
    QuestionHistory
)

router = APIRouter()


@router.get("/analytics/files")
def file_analytics():

    db = SessionLocal()

    try:

        pdf = (
            db.query(Document)
            .filter(
                Document.filename.like("%.pdf")
            )
            .count()
        )

        docx = (
            db.query(Document)
            .filter(
                Document.filename.like("%.docx")
            )
            .count()
        )

        pptx = (
            db.query(Document)
            .filter(
                Document.filename.like("%.pptx")
            )
            .count()
        )

        return {
            "pdf": pdf,
            "docx": docx,
            "pptx": pptx
        }

    finally:
        db.close()


@router.get("/analytics/questions")
def question_analytics():

    db = SessionLocal()

    try:

        total_questions = db.query(
            QuestionHistory
        ).count()

        return {
            "total_questions":
                total_questions
        }

    finally:
        db.close()
from fastapi import APIRouter

from app.database.connection import (
    SessionLocal
)

from app.database.models import (
    Document,
    QuestionHistory
)

router = APIRouter()


@router.get(
"/dashboard-stats"
)
def dashboard_stats():

    db = SessionLocal()

    try:

        total_documents = (
            db.query(Document)
            .count()
        )

        total_questions = (
            db.query(
                QuestionHistory
            )
            .count()
        )

        recent_questions = (

            db.query(
                QuestionHistory
            )

            .order_by(
                QuestionHistory.id.desc()
            )

            .limit(5)

            .all()
        )

        return {

            "documents":
            total_documents,

            "questions":
            total_questions,

            "recent_questions":
            [
                q.question
                for q in recent_questions
            ]
        }

    finally:

        db.close()
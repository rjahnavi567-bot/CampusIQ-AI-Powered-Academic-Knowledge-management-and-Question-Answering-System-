from fastapi import APIRouter
from collections import defaultdict

from app.database.connection import SessionLocal
from app.database.models import QuestionHistory

router = APIRouter()


@router.get("/history/grouped")
def grouped_history():

    db = SessionLocal()

    try:

        records = (
            db.query(QuestionHistory)
            .order_by(
                QuestionHistory.document_name,
                QuestionHistory.question
            )
            .all()
        )

        grouped = defaultdict(list)

        for item in records:

            grouped[
                item.document_name
            ].append(
                {
                    "id": item.id,
                    "question": item.question,
                    "created_at":
                    item.created_at
                }
            )

        return grouped

    finally:
        db.close()
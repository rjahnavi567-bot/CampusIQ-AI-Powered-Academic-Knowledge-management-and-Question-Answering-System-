from fastapi import APIRouter
from app.database.connection import SessionLocal
from app.database.models import QuestionHistory

router = APIRouter()

@router.get("/questions/search")
def search_question(keyword:str):

    db = SessionLocal()

    results = (
        db.query(QuestionHistory)
        .filter(
            QuestionHistory.question.ilike(
                f"%{keyword}%"
            )
        )
        .all()
    )

    return results
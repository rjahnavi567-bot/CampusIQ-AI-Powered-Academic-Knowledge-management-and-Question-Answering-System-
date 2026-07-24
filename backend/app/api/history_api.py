from fastapi import APIRouter
from app.database.connection import SessionLocal
from app.database.models import QuestionHistory
from fastapi import Depends
from app.dependencies.auth_dependency import get_current_user
router = APIRouter()

@router.get("/history")
def history(
    current_user=Depends(get_current_user)
):
    db = SessionLocal()

    try:

        history = (
            db.query(QuestionHistory)
            .order_by(
                QuestionHistory.id.desc()
            )
            .all()
        )

        return history

    finally:
        db.close()


@router.delete("/history")
def clear_history():

    db = SessionLocal()

    try:

        deleted = db.query(
            QuestionHistory
        ).delete()

        db.commit()

        return {
            "message": "History cleared",
            "deleted_records": deleted
        }

    finally:
        db.close()
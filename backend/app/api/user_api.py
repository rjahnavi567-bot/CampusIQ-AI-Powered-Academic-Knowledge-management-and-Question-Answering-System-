from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import User
from app.schemas.user_schema import UserCreate



router = APIRouter()
@router.post("/users")
def create_user(user: UserCreate,
                db: Session = Depends(get_db)):

    new_user = User(
        name=user.name,
        role=user.role
    )

    db.add(new_user)
    db.commit()

    return {"message":"User Created"}

@router.get("/users")
def get_users(db: Session = Depends(get_db)):

    users = db.query(User).all()

    return users


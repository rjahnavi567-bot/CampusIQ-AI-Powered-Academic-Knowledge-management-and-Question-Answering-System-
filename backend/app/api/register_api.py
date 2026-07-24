from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database.connection import SessionLocal
from app.database.models import User

from app.auth.auth_service import hash_password

router = APIRouter(tags=["Authentication"])


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    confirm_password: str


@router.post("/register")
def register(request: RegisterRequest):

    db = SessionLocal()

    try:

        # ----------------------------
        # Password Match
        # ----------------------------
        if request.password != request.confirm_password:

            raise HTTPException(
                status_code=400,
                detail="Passwords do not match"
            )

        # ----------------------------
        # Password Length
        # ----------------------------
        if len(request.password) < 8:

            raise HTTPException(
                status_code=400,
                detail="Password must contain at least 8 characters"
            )

        # ----------------------------
        # Email Exists
        # ----------------------------
        existing = (
            db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        if existing:

            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        # ----------------------------
        # Create User
        # ----------------------------
        user = User(

            name=request.name,

            email=request.email,

            password=hash_password(request.password),

            role="Student",

            is_active=True

        )

        db.add(user)

        db.commit()

        db.refresh(user)

        return {

            "message": "Registration Successful"

        }

    finally:

        db.close()
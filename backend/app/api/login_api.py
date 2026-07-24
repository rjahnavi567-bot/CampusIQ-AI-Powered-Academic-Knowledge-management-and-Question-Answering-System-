from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database.connection import SessionLocal
from app.database.models import User

from app.auth.auth_service import verify_password
from app.auth.jwt_service import create_access_token

router = APIRouter(tags=["Authentication"])


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(request: LoginRequest):

    db = SessionLocal()

    try:

        user = (
            db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid Email"
            )

        if not verify_password(
            request.password,
            user.password
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid Password"
            )

        token = create_access_token(
            {
                "user_id": user.id,
                "email": user.email,
                "role": user.role
            }
        )

        return {
            "message": "Login Successful",
            "access_token": token,
            "token_type": "Bearer",
            "name": user.name,
            "role": user.role
        }

    finally:
        db.close()
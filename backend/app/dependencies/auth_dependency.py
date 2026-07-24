from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database.connection import SessionLocal
from app.database.models import User
from app.auth.jwt_service import verify_token

# Reads Authorization: Bearer <token>
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or Expired Token"
        )

    db = SessionLocal()

    try:

        user = (
            db.query(User)
            .filter(User.id == payload["user_id"])
            .first()
        )

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=403,
                detail="Account Disabled"
            )

        return user

    finally:
        db.close()
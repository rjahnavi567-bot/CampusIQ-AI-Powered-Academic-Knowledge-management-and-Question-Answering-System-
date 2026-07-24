from fastapi import APIRouter, Depends
from app.dependencies.auth_dependency import get_current_user

router = APIRouter(tags=["Authentication"])


@router.get("/me")
def current_user(
    user=Depends(get_current_user)
):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
    }
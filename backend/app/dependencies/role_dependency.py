from fastapi import Depends, HTTPException

from app.dependencies.auth_dependency import get_current_user


def require_roles(*allowed_roles):

    def role_checker(user=Depends(get_current_user)):

        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Permission Denied"
            )

        return user

    return role_checker
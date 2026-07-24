from fastapi import APIRouter, UploadFile, File
from app.services.upload.upload_manager import upload_manager
from fastapi import Depends
from app.dependencies.auth_dependency import get_current_user
router = APIRouter()


@router.post("/upload")
def upload(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user)
):
    """
    Upload endpoint.

    All business logic is handled by UploadManager.
    """

    return upload_manager.upload(
        file,
        current_user.id
    )
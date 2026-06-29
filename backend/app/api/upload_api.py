from fastapi import APIRouter, UploadFile, File
from app.services.upload.upload_manager import upload_manager

router = APIRouter()


@router.post("/upload")
def upload_file(file: UploadFile = File(...)):
    """
    Upload endpoint.

    All business logic is handled by UploadManager.
    """

    return upload_manager.upload(file)
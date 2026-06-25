from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.database.connection import SessionLocal
from app.database.models import Document

router = APIRouter()


@router.get("/documents/download/{document_id}")
def download_document(document_id: int):

    db = SessionLocal()

    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return FileResponse(
        path=document.file_path,
        filename=document.filename
    )
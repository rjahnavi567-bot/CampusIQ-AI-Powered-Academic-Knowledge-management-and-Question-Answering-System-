from fastapi import APIRouter
from app.services.pdf_service import extract_text_from_pdf

router = APIRouter()

@router.get("/extract/{filename}")
def extract_pdf(filename: str):

    path = f"uploads/{filename}"

    text = extract_text_from_pdf(path)

    return {
        "filename": filename,
        "characters": len(text),
        "preview": text[:1000]
    }
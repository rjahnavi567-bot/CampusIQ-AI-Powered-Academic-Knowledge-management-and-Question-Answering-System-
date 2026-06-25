from fastapi import APIRouter
from app.database.connection import SessionLocal
from app.database.models import Chunk

router = APIRouter()

@router.get("/chunks/count")
def chunk_count():

    db = SessionLocal()

    try:
        count = db.query(Chunk).count()

        return {
            "total_chunks": count
        }

    finally:
        db.close()

@router.get("/chunks")
def get_chunks():

    db = SessionLocal()

    chunks = db.query(Chunk).all()

    result = []

    for chunk in chunks:

        result.append({
            "id": chunk.id,
            "topic": chunk.topic,
            "source_file": chunk.source_file,
            "file_type": chunk.file_type
        })

    db.close()

    return result

@router.get("/chunks")
def get_chunks():

    db = SessionLocal()

    try:
        chunks = db.query(Chunk).all()

        return chunks

    finally:
        db.close()

@router.get("/chunks/document/{document_id}")
def get_document_chunks(document_id: int):

    db = SessionLocal()

    try:
        chunks = (
            db.query(Chunk)
            .filter(
                Chunk.document_id == document_id
            )
            .all()
        )

        return chunks

    finally:
        db.close()
from fastapi import APIRouter, HTTPException
from app.database.connection import SessionLocal
from app.database.models import Document, Chunk
from app.services.chroma_service import text_collection

router = APIRouter()


# ==========================
# GET ALL DOCUMENTS
# ==========================

@router.get("/documents")
def get_documents():

    db = SessionLocal()

    try:

        docs = (
            db.query(Document)
            .order_by(Document.filename)
            .all()
        )

        return docs

    finally:
        db.close()


# ==========================
# VIEW DOCUMENT URL
# ==========================

@router.get("/documents/{document_id}/view")
def view_document(document_id: int):

    db = SessionLocal()

    try:

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

        return {
            "filename": document.filename,
            "url":
            f"http://localhost:8000/uploads/{document.filename}"
        }

    finally:
        db.close()


# ==========================
# GET SINGLE DOCUMENT
# ==========================

@router.get("/documents/{document_id}")
def get_document(document_id: int):

    db = SessionLocal()

    try:

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

        return document

    finally:
        db.close()


@router.get(
    "/documents/{document_id}/page/{page_no}"
)
def open_document_page(
    document_id: int,
    page_no: int
):

    db = SessionLocal()

    try:

        document = (
            db.query(Document)
            .filter(
                Document.id == document_id
            )
            .first()
        )

        if not document:

            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

        return {
            "filename": document.filename,
            "url":
            f"http://localhost:8000/uploads/{document.filename}#page={page_no}"
        }

    finally:
        db.close()

# ==========================
# DELETE DOCUMENT
# ==========================

@router.delete("/documents/{document_id}")
def delete_document(document_id: int):

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

    db.query(Chunk).filter(
        Chunk.document_id == document_id
    ).delete()

    db.delete(document)

    db.commit()

    results = text_collection.get()

    ids_to_delete = []

    for i, metadata in enumerate(
        results["metadatas"]
    ):

        if (
            metadata.get("source_file")
            == document.filename
        ):

            ids_to_delete.append(
                results["ids"][i]
            )

    if ids_to_delete:

        text_collection.delete(
            ids=ids_to_delete
        )

    return {
        "message":
        "Document deleted successfully"
    }
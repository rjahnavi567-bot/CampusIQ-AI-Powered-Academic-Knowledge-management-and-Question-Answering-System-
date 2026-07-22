from fastapi import APIRouter, HTTPException
from app.database.connection import SessionLocal
from app.database.models import Document, Chunk
from app.services.chroma_service import text_collection
import os
import shutil

from app.database.models import (
    Document,
    Chunk,
    DocumentImage
)

from app.services.chroma_service import (
    text_collection,
    image_collection
)
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
f"http://localhost:8000/{document.file_path}"
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
f"http://localhost:8000/{document.file_path}#page={page_no}"
        }

    finally:
        db.close()

# ==========================
# DELETE DOCUMENT
# ==========================
@router.delete("/documents/{document_id}")
def delete_document(document_id: int):

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

        filename = document.filename
        file_path = document.file_path

        ###################################################
        # Delete text embeddings
        ###################################################

        results = text_collection.get()

        ids = []

        for i, metadata in enumerate(results["metadatas"]):

            if metadata.get("source_file") == filename:

                ids.append(results["ids"][i])

        if ids:

            text_collection.delete(ids=ids)

        ###################################################
        # Delete image embeddings
        ###################################################

        try:

            results = image_collection.get()

            ids = []

            for i, metadata in enumerate(results["metadatas"]):

                if metadata.get("source_file") == filename:

                    ids.append(results["ids"][i])

            if ids:

                image_collection.delete(ids=ids)

        except Exception:

            pass

        ###################################################
        # Delete image metadata
        ###################################################

        db.query(DocumentImage).filter(

            DocumentImage.document_id == document_id

        ).delete()

        ###################################################
        # Delete chunks
        ###################################################

        db.query(Chunk).filter(

            Chunk.document_id == document_id

        ).delete()

        ###################################################
        # Delete document row
        ###################################################

        db.delete(document)

        db.commit()

        ###################################################
        # Delete uploaded PDF
        ###################################################

        if file_path and os.path.exists(file_path):

            os.remove(file_path)

        ###################################################
        # Delete extracted images
        ###################################################

        image_folder = f"uploads/images/{document_id}"

        if os.path.exists(image_folder):

            shutil.rmtree(image_folder)

        return {

            "message": "Document deleted successfully"

        }

    finally:

        db.close()
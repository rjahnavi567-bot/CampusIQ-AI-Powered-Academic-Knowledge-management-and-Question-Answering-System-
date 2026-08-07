from fastapi import APIRouter, HTTPException
from app.database.connection import SessionLocal
from app.database.models import Document, Chunk
from app.services.chroma_service import text_collection
import os
import shutil
from app.services.document_cache import document_cache
from app.database.models import (
    Document,
    Chunk,
    DocumentImage
)
from app.services.trie_service import document_trie
from app.services.chroma_service import (
    text_collection,
    image_collection
)
from fastapi import Depends
from collections import defaultdict
from app.dependencies.auth_dependency import get_current_user
router = APIRouter()

from collections import defaultdict

from collections import defaultdict


@router.get("/documents/grouped")
def get_documents_grouped(
    current_user=Depends(get_current_user)
):
    db = SessionLocal()

    try:

        docs = (
            db.query(Document)
            .order_by(
                Document.parent_subject,
                Document.subject,
                Document.filename
            )
            .all()
        )

        grouped = defaultdict(list)

        for doc in docs:

            subject = (
                doc.subject
                if doc.subject
                else "Uncategorized"
            )

            grouped[subject].append(
                {
                    "id": doc.id,
                    "filename": doc.filename,
                    "subject": doc.subject,
                    "parent_subject": doc.parent_subject,
                    "status": doc.status,
                    "chunk_count": doc.chunk_count,
                    "created_at": doc.created_at
                }
            )

        # Convert dictionary into frontend-friendly list

        result = []

        for subject, documents in grouped.items():

            result.append(
                {
                    "subject": subject,
                    "documents": documents
                }
            )

        return result

    finally:
        db.close()
@router.get("/documents/suggestions")
def autocomplete(query: str):

    if not query:

        return []

    return document_trie.search_prefix(query)
@router.get("/documents/search")
def search_documents(query: str):

    if not query.strip():
        return []

    # 1. Exact search using HashMap
    exact = document_cache.get_document(query)

    if exact:
        return [exact]

    # 2. Partial search using PostgreSQL
    db = SessionLocal()

    try:

        documents = (
            db.query(Document)
            .filter(Document.filename.ilike(f"%{query}%"))
            .order_by(Document.filename)
            .all()
        )

        return documents

    finally:
        db.close()
# ==========================
# GET ALL DOCUMENTS
# ==========================

@router.get("/documents")
def get_documents(
    current_user=Depends(get_current_user)
):
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
        document_cache.remove_document(document.filename)

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
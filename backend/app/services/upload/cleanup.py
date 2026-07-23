from app.database.models import Chunk, DocumentImage
from app.services.chroma_service import (
    text_collection,
    image_collection
)
from app.database.models import Document
import shutil
import os
def cleanup_upload(db, document_id, filename, file_path):
    print("\n========================")
    print("RUNNING CLEANUP")
    print("========================")
    print("Document ID:", document_id)
    print("Filename:", filename)
    print("File Path:", file_path)

    print("\nRunning upload rollback...")

    # -------------------------
    # Delete SQL records
    # -------------------------

    db.query(Chunk).filter(
        Chunk.document_id == document_id
    ).delete()

    db.query(DocumentImage).filter(
        DocumentImage.document_id == document_id
    ).delete()

    db.query(Document).filter(
        Document.id == document_id
    ).delete()

    db.commit()

    # -------------------------
    # Delete Chroma Text
    # -------------------------

    try:

        results = text_collection.get()

        ids = []

        for i, meta in enumerate(results["metadatas"]):

            if meta.get("document_id") == document_id:

                ids.append(results["ids"][i])

        if ids:

            text_collection.delete(ids=ids)

            print(f"Deleted {len(ids)} text embeddings")

    except Exception as e:

        print("Text cleanup failed:", e)

    # -------------------------
    # Delete Chroma Images
    # -------------------------

    try:

        results = image_collection.get()

        ids = []

        for i, meta in enumerate(results["metadatas"]):

            if meta.get("document_id") == document_id:

                ids.append(results["ids"][i])

        if ids:

            image_collection.delete(ids=ids)

            print(f"Deleted {len(ids)} image embeddings")

    except Exception as e:

        print("Image cleanup failed:", e)

    # -------------------------
    # Delete uploaded pdf
    # -------------------------
    try:
        image_folder = f"uploads/images/{document_id}"

        print("Image folder exists:", os.path.exists(image_folder))
        print("Image folder:", os.path.abspath(image_folder))

        print("PDF exists:", os.path.exists(file_path))
        print("PDF:", os.path.abspath(file_path))

        if os.path.exists(image_folder):
            shutil.rmtree(image_folder)
            print("Deleted image folder")

        if os.path.exists(file_path):
            os.remove(file_path)
            print("Deleted PDF")
    except Exception as e:
        print("File cleanup failed:", e)
    # -------------------------
# Remove empty temp folder file
# -------------------------

    if os.path.exists(file_path):
        os.remove(file_path)


    print("Rollback completed.")
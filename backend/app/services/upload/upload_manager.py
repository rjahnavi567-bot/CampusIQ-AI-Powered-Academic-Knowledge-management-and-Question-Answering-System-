import os
import json
import shutil
import time

from fastapi import HTTPException

from app.database.connection import SessionLocal
from app.database.models import Document

from app.services.document_processor import extract_text
from app.services.chunk_storage_service import save_chunks
from app.services.text_storage_service import store_text_chunks
from app.services.image_storage_service import (
    save_images,
    store_images
)
from app.services.hash_service import generate_file_hash

from app.services.upload.file_validation import validate_file
from app.services.upload.document_initializer import (
    create_document,
    finalize_document,
    update_document_filename
)

from app.services.upload.duplicate_detector import (
    check_similarity
)

from app.services.upload.title_generator import (
    generate_document_title
)

from app.services.upload.text_pipeline import (
    process_text_pages
)

from app.services.upload.image_pipeline import (
    process_images
)

from app.services.upload.response_builder import (
    build_upload_response
)


class UploadManager:

    def upload(self, file):

        start_time = time.time()

        print(f"\nStarting Upload : {file.filename}")

        validation = validate_file(file)

        if not validation["valid"]:

            raise HTTPException(
                status_code=400,
                detail=validation["message"]
            )

        db = SessionLocal()

        try:

            os.makedirs(
                "uploads",
                exist_ok=True
            )

            file_path = f"uploads/{file.filename}"

            with open(file_path, "wb") as buffer:

                shutil.copyfileobj(
                    file.file,
                    buffer
                )

            # ------------------------------------
            # Generate Hash
            # ------------------------------------

            file_hash = generate_file_hash(
                file_path
            )

            print("File Hash :", file_hash)

            existing_document = (

                db.query(Document)

                .filter(
                    Document.file_hash == file_hash
                )

                .first()

            )

            if existing_document:

                os.remove(file_path)

                return {

                    "error":
                    "Duplicate document detected.",

                    "existing_document":
                    existing_document.filename,

                    "document_id":
                    existing_document.id,

                    "view_url":
                    f"/documents/{existing_document.id}/view"

                }

            # ------------------------------------
            # Create Database Record
            # ------------------------------------

            new_doc = create_document(

                db=db,

                filename=file.filename,

                file_path=file_path,

                file_hash=file_hash

            )

            document_id = new_doc.id

            print(
                f"Document ID : {document_id}"
            )

            # ------------------------------------
            # Extract Text
            # ------------------------------------

            print("Extracting text...")

            pages = extract_text(
                file_path
            )

            print(
                f"Pages Extracted : {len(pages)}"
            )

            # ------------------------------------
            # Process Images
            # ------------------------------------

            print("Processing Images...")

            images = process_images(

                file_path=file_path,

                document_id=document_id,

                pages=pages

            )

            print(
                f"Images Found : {len(images)}"
            )
                        # ------------------------------------
            # Generate Better Title
            # ------------------------------------

            print("Generating document title...")

            suggested_title, new_filename, new_file_path = (

                generate_document_title(

                    file_path=file_path,

                    pages=pages,

                    original_filename=file.filename

                )

            )

            file_path = new_file_path

            update_document_filename(

                db=db,

                document=new_doc,

                new_filename=new_filename,

                fnew_ile_path=file_path

            )

            print("New Filename :", new_filename)

            # ------------------------------------
            # Text Pipeline
            # ------------------------------------

            print("Creating semantic chunks...")

            chunks, content_signature = process_text_pages(

                pages=pages,

                filename=new_filename

            )

            print(

                f"Chunks Created : {len(chunks)}"

            )

            # ------------------------------------
            # Similarity Detection
            # ------------------------------------

            print("Checking document similarity...")

            embedding, highest_similarity, similar_document = (

                check_similarity(

                    db,

                    content_signature

                )

            )

            if highest_similarity > 0.95:

                db.delete(new_doc)

                db.commit()

                os.remove(file_path)

                return {

                    "error":

                    "Very similar document already exists.",

                    "similarity":

                    round(

                        highest_similarity * 100,

                        2

                    ),

                    "existing_document":

                    similar_document.filename,

                    "document_id":

                    similar_document.id,

                    "view_url":

                    f"/documents/{similar_document.id}/view"

                }

            similarity_warning = None

            if (

                highest_similarity >= 0.90

                and similar_document

            ):

                similarity_warning = {

                    "similarity":

                    round(

                        highest_similarity * 100,

                        2

                    ),

                    "existing_document":

                    similar_document.filename,

                    "document_id":

                    similar_document.id

                }

            # ------------------------------------
            # Save Signature + Embedding
            # ------------------------------------

            new_doc.content_signature = (

                str(content_signature)

                .replace("\x00", "")

                .replace("\u0000", "")

            )

            new_doc.embedding = json.dumps(

                embedding

            )

            db.commit()

            print("Similarity Check Complete.")
                        # ------------------------------------
            # Save Chunks
            # ------------------------------------

            print("Saving chunks...")

            save_chunks(

                document_id,

                chunks

            )

            # ------------------------------------
            # Update Database
            # ------------------------------------

            finalize_document(

                db=db,

                document=new_doc,

                chunk_count=len(chunks)

            )

            # ------------------------------------
            # Store Text Embeddings
            # ------------------------------------

            print("Uploading text embeddings to Chroma...")

            store_text_chunks(

                document_id,

                chunks

            )

            # ------------------------------------
            # Store Image Embeddings
            # ------------------------------------

            print("Uploading image embeddings to Chroma...")

            save_images(db, document_id, images)
            store_images(images, document_id)

            print(

                f"Stored {len(images)} images."

            )

            elapsed = round(

                time.time() - start_time,

                2

            )

            print(

                f"\nUpload Finished in {elapsed} seconds."

            )

            # ------------------------------------
            # Build API Response
            # ------------------------------------

            return build_upload_response(

                original_filename=file.filename,

                stored_filename=new_filename,

                suggested_title=suggested_title,

                chunks=chunks,

                images=images,

                similarity_warning=similarity_warning

            )

        except Exception as e:

            db.rollback()

            print("\nUPLOAD FAILED")

            print(str(e))

            raise HTTPException(

                status_code=500,

                detail=str(e)

            )

        finally:

            db.close()


upload_manager = UploadManager()
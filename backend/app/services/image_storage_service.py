from app.database.models import DocumentImage
from app.services.chroma_service import image_collection
import os


def save_images(db, document_id, images):
    """
    Save image metadata into MySQL.
    """

    for image in images:

        record = DocumentImage(
            document_id=document_id,
            image_path=image["path"],
            page_no=image["page_no"],
            caption=image["caption"]
        )

        db.add(record)

    db.commit()


def store_images(images, document_id):
    """
    Store image captions + OCR into ChromaDB.
    """

    for image in images:

        image_collection.add(

            ids=[
                f"image_{document_id}_{os.path.basename(image['path'])}"
            ],

            documents=[
                (
                    "Image Caption:\n"
                    + image["caption"]
                    + "\n\nOCR:\n"
                    + image["ocr_text"]
                )
            ],

            metadatas=[
                {
                    "document_id": document_id,
                    "type": "image",
                    "page_no": image["page_no"],
                    "image_path": image["path"],
                    "caption": image["caption"],
                    "source_file": image["source_file"]
                }
            ]
        )

    print(f"Stored {len(images)} images into Image Collection.")
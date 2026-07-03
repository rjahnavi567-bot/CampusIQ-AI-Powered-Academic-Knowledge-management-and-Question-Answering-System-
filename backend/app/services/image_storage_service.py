from app.database.models import DocumentImage
from app.services.chroma_service import image_collection
from app.services.image_embedding_service import embed_image
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

    caption=image.get("caption", ""),

    title=image.get("title", ""),

    image_hash=image.get("image_hash", ""),

    source_file=image.get("source_file", "")

)

        db.add(record)
    print("\nSaving image metadata...")

    for image in images:
        print(image["path"])

    db.commit()
    print("Images saved:", len(images))


def store_images(images, document_id):
    """
    Store image metadata into ChromaDB.

    """
    
    for image in images:
        print(
            image["title"],
            len(image["clip_embedding"])
        )


        image_collection.add(

            ids=[
                f"image_{document_id}_{image['image_hash']}"
            ],

            documents=[
(
f"""
IMAGE_HASH:
{image.get("image_hash","")}

TITLE:
{image.get("title","")}

CAPTION:
{image.get("caption","")}

OCR:
{image.get("ocr_text","")}

VISION:
{image.get("vision","")}

PAGE CONTEXT:
{image.get("page_text","")}
"""
)
],

            embeddings=[image["clip_embedding"]],
            metadatas=[

                {

                    "document_id": document_id,

                    "type": "image",

                    "page_no": image["page_no"],

                    "image_path": image["path"],

                    "caption": image.get("caption", ""),

                    "title": image.get("title", ""),

                    "image_hash": image.get("image_hash", ""),

                    "source_file": image.get("source_file", ""),

                    "file_type": image.get("file_type", "")

                }

            ]
        )

    print(f"Stored {len(images)} images.")
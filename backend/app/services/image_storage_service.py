from app.database.models import DocumentImage
from app.services.chroma_service import image_collection


# ==========================================================
# SAVE IMAGE METADATA TO MYSQL
# ==========================================================

def save_images(db, document_id, images):
    """
    Save image metadata into MySQL.
    """

    print("\nSaving image metadata...")

    for image in images:

        print(f"Saving : {image.path}")

        record = DocumentImage(

            document_id=document_id,

            image_path=image.path,

            page_no=image.page_no,

            caption=image.caption,

            title=image.title,

            image_hash=str(image.md5_hash),

            source_file=image.source_file,

            category=image.category,

            classification_confidence=image.classification_confidence,

            confidence_score=image.confidence_score

        )

        db.add(record)

    db.commit()

    print(f"Images saved : {len(images)}")


# ==========================================================
# STORE IMAGE TEXT EMBEDDINGS INTO CHROMADB
# ==========================================================

def store_images(images, document_id):
    """
    Store IMAGE TEXT embeddings (384-d BGE)
    into ChromaDB for semantic retrieval.
    """

    if not images:

        print("No images to store.")

        return

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for index, image in enumerate(images):

        # Skip invalid embeddings
        if (
            not hasattr(image, "text_embedding")
            or image.text_embedding is None
            or len(image.text_embedding) != 384
        ):
            continue

        ids.append(
            f"image_{document_id}_page_{image.page_no}_{index}"
        )

        documents.append(
f"""
MD5_HASH:
{image.md5_hash}

PERCEPTUAL_HASH:
{image.perceptual_hash}

TITLE:
{image.title}

CAPTION:
{image.caption}

OCR:
{image.ocr_text}

VISION:
{image.vision}

PAGE_CONTEXT:
{image.page_context}

SEARCH_TEXT:
{image.search_text}
"""
        )

        # Store BGE embedding (384)
        embeddings.append(
            image.text_embedding
        )

        metadatas.append({

            "document_id": document_id,

            "type": "image",

            "page_no": image.page_no,

            "image_path": image.path,

            "caption": image.caption,

            "title": image.title,

            "category": image.category,

            "classification_confidence": float(
                image.classification_confidence
            ),

            "confidence_score": float(
                image.confidence_score
            ),

            "md5_hash": str(image.md5_hash),

            "perceptual_hash": str(image.perceptual_hash),

            "source_file": image.source_file,

            "file_type": image.file_type

        })

    if len(ids) == 0:

        print("No valid text embeddings found.")

        return

    image_collection.add(

        ids=ids,

        documents=documents,

        embeddings=embeddings,

        metadatas=metadatas

    )

    print("\n==============================")
    print("STAGE 10.3 : CHROMADB STORAGE")
    print("==============================")
    print(f"Stored Images : {len(ids)}")
    print("Embedding Type : BGE Text")
    print("Dimension      : 384")
    print("==============================")
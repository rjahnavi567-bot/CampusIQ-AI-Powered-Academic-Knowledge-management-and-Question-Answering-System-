from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

import uuid

from app.config.qdrant import client


# ==========================================================
# COLLECTION NAME
# ==========================================================

COLLECTION_NAME = "image_vectors"


# ==========================================================
# CREATE COLLECTION
# ==========================================================

def create_collection():

    collections = client.get_collections()

    names = [

        collection.name

        for collection in collections.collections

    ]

    if COLLECTION_NAME in names:

        print("Qdrant collection already exists.")

        return

    client.create_collection(

        collection_name=COLLECTION_NAME,

        vectors_config=VectorParams(

            size=512,

            distance=Distance.COSINE

        )

    )

    print("Qdrant Image Collection Created")


# ==========================================================
# STORE CLIP EMBEDDINGS
# ==========================================================

def store_images(images):

    points = []

    for image in images:

        if (

            not hasattr(image, "clip_embedding")

            or image.clip_embedding is None

            or len(image.clip_embedding) != 512

        ):

            continue

        payload = {

            "document_id": image.document_id,

            "page_no": image.page_no,

            "filename": image.filename,

            "path": image.path,

            "caption": image.caption,

            "title": image.title,

            "ocr_text": image.ocr_text,

            "page_context": image.page_context,

            "category": image.category,

            "source_file": image.source_file,

            "search_text": image.search_text

        }

        points.append(

            PointStruct(

                id=str(uuid.uuid4()),

                vector=image.clip_embedding,

                payload=payload

            )

        )

    if len(points) == 0:

        print("No CLIP embeddings found.")

        return

    client.upsert(

        collection_name=COLLECTION_NAME,

        points=points

    )

    print("\n==============================")
    print("STAGE 10.3 : QDRANT STORAGE")
    print("==============================")
    print(f"Stored Images : {len(points)}")
    print("Embedding Type : CLIP")
    print("Dimension      : 512")
    print("==============================")
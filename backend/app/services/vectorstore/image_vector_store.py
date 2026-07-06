from qdrant_client.models import Distance
from qdrant_client.models import VectorParams
from qdrant_client.models import PointStruct
import uuid
from app.config.qdrant import client


COLLECTION_NAME = "image_vectors"
def store_images(images):

    points = []

    for image in images:

        if not image.clip_embedding:
            continue

        payload = {

            "page_no": image.page_no,

            "caption": image.caption,

            "ocr_text": image.ocr_text,

            "category": image.category,

            "filename": image.filename,

            "path": image.path,

            "page_context": image.page_context,

            "search_text": image.search_text,

            "document_id": image.document_id

        }

        points.append(

            PointStruct(

                id=str(uuid.uuid4()),

                vector=image.clip_embedding,

                payload=payload

            )

        )

    if not points:

        print("No image embeddings found.")

        return

    client.upsert(

        collection_name=COLLECTION_NAME,

        points=points

    )

    print(f"Stored {len(points)} images.")

def create_collection():

    collections = client.get_collections()

    names = [

        c.name

        for c in collections.collections

    ]

    if COLLECTION_NAME in names:

        print("Collection already exists.")

        return

    client.create_collection(

        collection_name=COLLECTION_NAME,

        vectors_config=VectorParams(

            size=512,

            distance=Distance.COSINE

        )

    )

    print("Image collection created.")
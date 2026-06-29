import json

from app.services.hash_service import generate_file_hash
from app.services.embedding_service1 import create_embedding
from app.services.similarity_service1 import cosine_similarity

from app.database.models import Document


def check_duplicate_hash(db, file_path):
    """
    Checks if the uploaded file already exists using SHA256 hash.
    """

    file_hash, existing_document = check_duplicate_hash(
    db,
    file_path
)

    return file_hash, existing_document


def check_similarity(db, content_signature):
    """
    Checks semantic similarity using stored embeddings.
    """

    embedding = create_embedding(content_signature[:4000])

    existing_docs = (
        db.query(Document)
        .filter(Document.embedding != None)
        .all()
    )

    highest_similarity = 0
    similar_document = None

    for doc in existing_docs:

        try:

            old_embedding = json.loads(doc.embedding)

            similarity = cosine_similarity(
                embedding,
                old_embedding
            )

            if similarity > highest_similarity:

                highest_similarity = similarity
                similar_document = doc

        except Exception:
            continue

    return embedding, highest_similarity, similar_document
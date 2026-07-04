import numpy as np

from app.services.image_embedding_service import (
    embed_text_for_image_search
)


def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def rerank_images(question, image_chunks):

    if not image_chunks:
        return []

    query_embedding = embed_text_for_image_search(question)

    for chunk in image_chunks:

        image_embedding = chunk["metadata"].get("clip_embedding")

        if image_embedding is None:
             score = 0
        else:
            score = cosine_similarity(
        query_embedding,
        image_embedding
    )

        chunk["clip_score"] = float(score)

    image_chunks.sort(

        key=lambda x: x["clip_score"],

        reverse=True

    )

    return image_chunks
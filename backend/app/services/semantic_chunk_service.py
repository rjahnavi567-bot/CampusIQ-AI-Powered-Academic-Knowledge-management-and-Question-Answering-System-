from app.services.embedding_service import get_embedding
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def create_semantic_chunks(paragraphs):

    chunks = []

    current_chunk = paragraphs[0]

    current_embedding = get_embedding(paragraphs[0])

    for para in paragraphs[1:]:

        para_embedding = get_embedding(para)

        similarity = cosine_similarity(
            [current_embedding],
            [para_embedding]
        )[0][0]

        print("Similarity:", similarity)

        if similarity > 0.6:

            current_chunk += "\n\n" + para

        else:

            chunks.append(current_chunk)

            current_chunk = para

            current_embedding = para_embedding

    chunks.append(current_chunk)

    return chunks
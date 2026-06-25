from app.services.embedding_service import generate_embedding
from app.services.similarity_service import calculate_similarity
from app.services.heading_detector import is_heading
SIMILARITY_THRESHOLD = 0.75

def create_semantic_chunks(paragraphs):

    chunks = []

    current_chunk = paragraphs[0]

    current_embedding = generate_embedding(
        current_chunk
    )

    for paragraph in paragraphs[1:]:
        if is_heading(paragraph):

            chunks.append(current_chunk)

            current_chunk = paragraph

            continue

        paragraph_embedding = generate_embedding(
            paragraph
        )

        score = calculate_similarity(
            current_embedding,
            paragraph_embedding
        )

        if score > SIMILARITY_THRESHOLD:

            current_chunk += "\n\n" + paragraph

        else:

            chunks.append(current_chunk)

            current_chunk = paragraph

            current_embedding = paragraph_embedding

    chunks.append(current_chunk)

    return chunks


import re
import numpy as np

from app.services.embedding_service import get_embeddings
from app.services.heading_detector import is_heading

SIMILARITY_THRESHOLD = 0.35
MAX_WORDS = 600
OVERLAP_WORDS = 20


def cosine_similarity(v1, v2):

    return np.dot(v1, v2) / (
        np.linalg.norm(v1)
        * np.linalg.norm(v2)
    )
def create_semantic_chunks(text):

    text = text.replace("\x00", "")

    from app.services.block_extractor import (
    extract_blocks,
    build_sections
)
    blocks = extract_blocks(text)

    sections = build_sections(blocks)

    paragraphs=[]

    section_headings=[]

    for section in sections:

        words=section["text"].split()

        for i in range(0,len(words),150):

            paragraphs.append(
            " ".join(words[i:i+150])
        )

            section_headings.append(
            section["heading"]
        )
    print("Text length:", len(text))
    print("Paragraph Count:", len(paragraphs))

    if len(paragraphs) == 0:
        print("No paragraphs found.")
        return []

    print("Generating embeddings...")

    embeddings = get_embeddings(
        paragraphs
    )

    print("Embeddings generated.")

    chunks = []

    current_chunk = ""
    current_heading = ""
    previous_embedding = None

    chunk_index = 1
    similarity = 0.0

    for i, para in enumerate(paragraphs):

        current_heading = section_headings[i]

        para = para.strip()

        if len(para) < 5:
            continue

        embedding = embeddings[i]

        # ------------------------
        # HEADING DETECTED
        # ------------------------
        if is_heading(para):

            if current_chunk:

                topic = (
                    current_heading
                    if current_heading
                    else current_chunk.split(".")[0][:100]
                )

                chunks.append({
                    "chunk_index": chunk_index,
                    "heading": current_heading,
                    "topic": topic,
                    "content": current_chunk,
                    "keywords": [],
                    "word_count": len(
                        current_chunk.split()
                    ),
                    "similarity_score": round(
                        float(similarity),
                        4
                    ),
                    "section":current_heading,
                })

                chunk_index += 1

            current_heading = para
            current_chunk = para
            previous_embedding = embedding
            similarity = 0.0

            continue

        # ------------------------
        # FIRST PARAGRAPH
        # ------------------------
        if previous_embedding is None:

            current_chunk = para
            previous_embedding = embedding
            similarity = 1.0

            continue

        # ------------------------
        # COSINE SIMILARITY
        # ------------------------
        similarity = cosine_similarity(
            previous_embedding,
            embedding
        )

        current_words = len(
            current_chunk.split()
        )

        para_words = len(
            para.split()
        )

        # ------------------------
        # MERGE PARAGRAPHS
        # ------------------------
        if (
            similarity > SIMILARITY_THRESHOLD
            and
            (
                current_words
                + para_words
            ) <= MAX_WORDS
        ):

            current_chunk += (
                "\n\n" + para
            )

        # ------------------------
        # CREATE NEW CHUNK
        # ------------------------
        else:

            topic = (
                current_heading
                if current_heading
                else current_chunk.split(".")[0][:100]
            )

            chunks.append({
                "chunk_index": chunk_index,
                "heading": current_heading,
                "topic": topic,
                "content": current_chunk,
                "keywords": [],
                "word_count": len(
                    current_chunk.split()
                ),
                "similarity_score": round(
                    float(similarity),
                    4
                ),
                "section":current_heading,
            })

            chunk_index += 1

            overlap_words = (
                current_chunk
                .split()
                [-OVERLAP_WORDS:]
            )

            current_chunk = (
                " ".join(
                    overlap_words
                )
                + "\n\n"
                + para
            )

        previous_embedding = embedding

    # ------------------------
    # LAST CHUNK
    # ------------------------
    if current_chunk:

        topic = (
            current_heading
            if current_heading
            else current_chunk.split(".")[0][:100]
        )

        chunks.append({
            "chunk_index": chunk_index,
            "heading": current_heading,
            "topic": topic,
            "content": current_chunk,
            "keywords": [],
            "word_count": len(
                current_chunk.split()
            ),
            "similarity_score": round(
                float(similarity),
                4
            ),
            "section":current_heading,
        })

    print("\n===== CHUNKS CREATED =====")
    print("TOTAL CHUNKS:", len(chunks))

    if len(chunks) == 0:
        return []

    avg_words = (
        sum(
            chunk["word_count"]
            for chunk in chunks
        )
        / len(chunks)
    )

    print(
        "Average chunk size:",
        round(avg_words)
    )

    return chunks
from app.services.chunk_service import create_semantic_chunks


def process_text_pages(pages, filename):
    """
    Extract semantic chunks from all pages.

    Returns:
        chunks
        content_signature
    """

    chunks = []

    content_signature = ""

    for page in pages:

        text = (
            page["text"]
            .replace("\x00", "")
            .replace("\u0000", "")
            .strip()
        )

        if not text:
            continue

        content_signature += text[:1000] + "\n"

        page_chunks = create_semantic_chunks(text)

        for chunk in page_chunks:

            chunk["page_no"] = page["page_no"]

            chunk["source_file"] = filename

            chunks.append(chunk)

    return chunks, content_signature
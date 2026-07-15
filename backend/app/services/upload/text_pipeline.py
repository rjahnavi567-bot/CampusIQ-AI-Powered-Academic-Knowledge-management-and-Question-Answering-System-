import os

from app.services.chunk_service import create_semantic_chunks


def process_text_pages(pages, filename):
    """
    Extract semantic chunks from all pages.

    Returns
    -------
    chunks
    content_signature
    """

    chunks = []

    content_signature = ""

    # Detect extension once
    file_type = os.path.splitext(filename)[1].lower()
    print("\n===== TEXT PAGES =====")
    print("Total Pages:", len(pages))

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
        print(
    f"Page {page['page_no']} -> "
    f"{len(page_chunks)} chunks"
)

        for chunk in page_chunks:

            chunk["page_no"] = page["page_no"]

            chunk["source_file"] = filename

            # NEW
            chunk["file_type"] = file_type

            chunks.append(chunk)
        print(f"\nPage {page['page_no']}")
        print("Text Length:", len(page["text"]))
        print(page["text"][:200])
    print("\n===== FIRST CHUNK =====")
    print(len(chunks))

    if chunks:
        print(chunks[0])
    else:
        print("No chunks generated.")
    return chunks, content_signature
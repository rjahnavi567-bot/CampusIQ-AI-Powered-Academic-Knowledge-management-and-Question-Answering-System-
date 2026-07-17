import os
from app.services.statistics import stats
from app.services.statistics.timer import Timer
from app.services.chunk_service import create_semantic_chunks
from app.services.statistics import collector
def process_text_pages(pages, filename):
    """
    Extract semantic chunks from all pages.

    Returns
    -------
    chunks
    content_signature
    """
    text_timer = Timer()
    chunk_timer = Timer()

    text_timer.start()

    chunks = []

    content_signature = ""

    # Detect extension once
    file_type = os.path.splitext(filename)[1].lower()
    print("\n===== TEXT PAGES =====")
    print("Total Pages:", len(pages))
    page_count = 0
    word_count = 0
    paragraph_count = 0
    chunk_count = 0

    for page in pages:

        text = (
            page["text"]
            .replace("\x00", "")
            .replace("\u0000", "")
            .strip()
        )
        page_count += 1

        if not text:
            continue
        words = text.split()

        word_count += len(words)

        paragraphs = [
    p for p in text.split("\n\n")
    if p.strip()
]

        paragraph_count += len(paragraphs)

        content_signature += text[:1000] + "\n"
        chunk_timer.start()

        page_chunks = create_semantic_chunks(text)
        chunk_time = chunk_timer.stop()

        collector.add_time(
    "Chunking Time",
    chunk_time
)
        
        print(
    f"Page {page['page_no']} -> "
    f"{len(page_chunks)} chunks"
)

        for chunk in page_chunks:
            chunk_count += 1

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
    text_time = text_timer.stop()

    collector.increment(
    "Total Pages Processed",
    page_count
)

    collector.increment(
    "Total Words Extracted",
    word_count
)

    collector.increment(
    "Total Paragraphs Identified",
    paragraph_count
)

    collector.increment(
    "Total Semantic Chunks Generated",
    chunk_count
)

    collector.add_time(
    "Text Extraction Time",
    text_time
)
    return chunks, content_signature
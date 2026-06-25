from app.database.connection import SessionLocal
from app.database.models import Chunk


def save_chunks(document_id, chunks):

    db = SessionLocal()

    try:
        for chunk in chunks:
            clean_topic = str(chunk["topic"]).replace("\x00", "")

            clean_content = str(chunk["content"]).replace("\x00", "")

            clean_keywords = ", ".join(
    chunk.get("keywords", [])
).replace("\x00", "")

            new_chunk = Chunk(
    document_id=document_id,
    topic=clean_topic,
    keywords=clean_keywords,
    source_file=chunk.get("source_file", "unknown"),
    file_type=chunk["file_type"],
    chunk_text=clean_content,
    page_no=chunk.get("page_no", 1),
    similarity_score=str(
        chunk.get(
            "similarity_score",
            0
        ))
)
            for field_name, value in {
    "topic": chunk["topic"],
    "content": chunk["content"],
    "keywords": ", ".join(chunk.get("keywords", []))
}.items():

                if "\x00" in str(value):
                    print(f"NUL FOUND IN {field_name}")
            db.add(new_chunk)

        db.commit()

    except Exception as e:
       db.rollback()
       raise e

    finally:
        db.close()
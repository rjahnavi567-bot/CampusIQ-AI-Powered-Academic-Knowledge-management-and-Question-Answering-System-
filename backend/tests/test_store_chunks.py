from app.services.chunk_storage_service import save_chunks

sample_chunks = [
    {
        "topic": "Introduction",
        "keywords": ["data", "mining"],
        "content": "Data mining is the process of discovering patterns.",
        "source_file": "test.pdf",
        "file_type": "pdf"
    }
]

save_chunks(1, sample_chunks)

print("Chunks saved successfully")
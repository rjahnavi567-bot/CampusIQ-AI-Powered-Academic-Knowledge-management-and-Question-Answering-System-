import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

# -----------------------------
# TEXT COLLECTION (384-dim)
# -----------------------------
text_collection = client.get_or_create_collection(
    name="academic_text"
)

# -----------------------------
# IMAGE COLLECTION (512-dim)
# -----------------------------
image_collection = client.get_or_create_collection(
    name="academic_images"
)
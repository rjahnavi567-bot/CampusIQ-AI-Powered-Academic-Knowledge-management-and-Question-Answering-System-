import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

# Text embeddings - 384
text_collection = client.get_or_create_collection(
    name="academic_text"
)

# Image CLIP embeddings -512
image_collection = client.get_or_create_collection(
    name="academic_images"
)
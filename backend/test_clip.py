from app.services.clip_service import create_image_embedding

embedding = create_image_embedding(
    "uploads/images/88/pdf_24_0.jpeg"
)

print(len(embedding))

print(embedding[:10])
from app.services.image_v2.doclayout.service import classify_document_image

image = r"uploads/test.png"

results = classify_document_image(image)

print(results)
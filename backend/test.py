from app.services.image_v2.siglip.service import classify

image = r"C:\Users\reddy\AI-Academic-System\backend\uploads\text.png"

result = classify(image)

print(result)
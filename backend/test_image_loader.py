from app.services.image_loader import load_image

image_path = "uploads/images/88/pdf_24_0.jpeg"

img = load_image(image_path)

print("PASS")
print("Size:", img.size)
print("Mode:", img.mode)
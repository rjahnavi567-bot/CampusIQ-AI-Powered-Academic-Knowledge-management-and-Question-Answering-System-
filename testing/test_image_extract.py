from app.services.document_processor import extract_text

text = extract_text("uploads/sample1.png")

print(text)
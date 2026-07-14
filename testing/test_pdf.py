from app.services.pdf_service import extract_text_from_pdf

pdf_path = "uploads/Who Moved My Cheese.pdf"

text = extract_text_from_pdf(pdf_path)

print(text[:2000])
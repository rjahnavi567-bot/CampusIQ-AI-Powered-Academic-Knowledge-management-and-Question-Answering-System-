import os


print(os.path.exists("uploads/Hello everyone.docx"))
import os

print("Current Directory:", os.getcwd())
print("Exists:", os.path.exists("uploads/Hello everyone.docx"))
print("Exists:", os.path.exists("app/uploads/Hello everyone.docx"))
from app.services.document_processor import extract_text

text = extract_text("uploads/Hello everyone.docx")

print(text)
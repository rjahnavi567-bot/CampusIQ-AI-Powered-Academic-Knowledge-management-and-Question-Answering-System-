import fitz
import cv2

from app.services.image_v2.detector import detect_layout


pdf = fitz.open("data mining Book.pdf")

page = pdf.load_page(0)

pix = page.get_pixmap(matrix=fitz.Matrix(2,2))

pix.save("page.png")


boxes = detect_layout("page.png")

print()

print("Detected:")

for b in boxes:

    print(b)
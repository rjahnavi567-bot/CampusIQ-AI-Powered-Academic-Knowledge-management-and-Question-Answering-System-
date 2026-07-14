from app.services.image_v2.page_renderer import render_pdf

pages = render_pdf(
    "uploads/data mining Book.pdf"
)

print(len(pages))

print(pages[0]["page_no"])

print(pages[0]["image"].shape)
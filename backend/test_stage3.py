from app.services.image_v2.page_renderer import render_pdf
from app.services.image_v2.region_detector import detect_regions

pages = render_pdf(
    "uploads/data mining Book.pdf"
)

for page in pages[:5]:

    regions = detect_regions(
        page["image"]
    )

    print(

        page["page_no"],

        len(regions)

    )
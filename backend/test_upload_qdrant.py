from app.services.image_v2.models import ImageCandidate
from app.services.image_v2.qdrant_service import upload_images

img = ImageCandidate(

    path="page.png",

    page_no=1,

    category="figure",

    bbox=(0,0,10,10),

    width=100,

    height=100
)

img.document_id = 5

img.caption = "Data integration"

img.ocr_text = "Data Cleaning"

img.page_context = "Chapter 3"

img.search_text = "Data integration Data Cleaning Chapter 3"

img.clip_embedding = [0.01]*512

upload_images([img])
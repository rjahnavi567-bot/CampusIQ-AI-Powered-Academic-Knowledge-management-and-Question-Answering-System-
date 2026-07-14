from app.services.image_v2.models import ImageCandidate

from app.services.vectorstore.image_vector_store import (
    store_images
)

img = ImageCandidate(

    path="sample.png",

    page_no=10,

    category="diagram",

    bbox=None,

    width=100,

    height=100

)

img.caption = "Data integration diagram"

img.ocr_text = "Data cleaning Data integration"

img.page_context = "Chapter about preprocessing."

img.search_text = (
    img.caption +
    "\n" +
    img.ocr_text +
    "\n" +
    img.page_context
)

img.filename = "sample.png"

img.document_id = 1

img.clip_embedding = [0.1] * 512

store_images([img])
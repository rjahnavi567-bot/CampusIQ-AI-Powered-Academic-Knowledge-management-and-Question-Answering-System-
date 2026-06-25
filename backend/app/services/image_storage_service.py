from app.database.models import (
    DocumentImage
)

def save_images(
    db,
    document_id,
    images
):

    for image in images:

        record = DocumentImage(

            document_id=document_id,

            image_path=image["path"],

            page_no=image["page_no"],

            caption=image["caption"]
        )

        db.add(record)

    db.commit()
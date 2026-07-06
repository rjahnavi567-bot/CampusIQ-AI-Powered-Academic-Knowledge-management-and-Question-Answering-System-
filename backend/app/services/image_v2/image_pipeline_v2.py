import os

from app.services.image_v2.extractor import ImageExtractor


def process_images_v2(

        file_path,

        document_id

):

    extension = os.path.splitext(

        file_path

    )[1].lower()

    if extension != ".pdf":

        raise Exception(

            "Stage-1 currently supports PDF only."

        )

    extractor = ImageExtractor(

        document_id

    )

    images = extractor.extract(

        file_path

    )

    print()

    print("="*60)

    print("STAGE 1")

    print("="*60)

    print()

    print(

        "Candidates Found:",

        len(images)

    )

    for img in images:

        print(

            img.source,

            img.page_no,

            os.path.basename(img.path)

        )

    print()

    return images
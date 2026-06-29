from collections import defaultdict


def merge_page_text_and_images(pages, images):
    """
    pages:
    [
        {
            "page_no": 1,
            "text": "..."
        }
    ]

    images:
    [
        {
            "page_no": 1,
            "caption": "...",
            "ocr_text": "..."
        }
    ]
    """

    images_by_page = defaultdict(list)

    for image in images:

        images_by_page[
            image["page_no"]
        ].append(image)

    merged_pages = []

    for page in pages:

        page_text = page["text"]

        page_number = page["page_no"]

        page_images = images_by_page.get(
            page_number,
            []
        )

        if page_images:

            page_text += "\n\n"

            page_text += "=" * 60

            page_text += "\nIMAGE INFORMATION\n"

            page_text += "=" * 60 + "\n\n"

            for index, image in enumerate(page_images, start=1):

                page_text += (
                    f"Image {index}\n\n"
                )

                page_text += (
                    "Caption:\n"
                )

                page_text += (
                    image["caption"]
                    + "\n\n"
                )

                ocr = image["ocr_text"].strip()

                if not ocr:

                    ocr = "No visible text."

                page_text += (
                    "Visible Text:\n"
                )

                page_text += (
                    ocr
                    + "\n\n"
                )

        merged_pages.append(

            {
                "page_no": page_number,
                "text": page_text
            }

        )

    return merged_pages
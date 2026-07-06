import os


def build_metadata(image, page_context=""):

    caption = image.get("caption", "").strip()

    ocr = image.get("ocr_text", "").strip()

    metadata = {

        "page_no": image["page_no"],

        "path": image["path"],

        "source_file": image.get("source_file", ""),

        "caption": caption,

        "ocr_text": ocr,

        "page_context": page_context,

        "category": image.get("category", ""),

        "image_hash": image.get("image_hash", ""),

        "filename": os.path.basename(image["path"])

    }

    metadata["search_text"] = "\n".join(

        part

        for part in [

            caption,

            ocr,

            page_context

        ]

        if part

    )

    return metadata
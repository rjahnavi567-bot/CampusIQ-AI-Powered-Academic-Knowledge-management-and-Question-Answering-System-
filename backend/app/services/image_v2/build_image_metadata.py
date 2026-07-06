from app.services.image_v2.metadata_builder import build_metadata


def build_all_metadata(images, page_lookup):

    metadata = []

    for image in images:

        page_text = page_lookup.get(

            image["page_no"],

            ""

        )

        metadata.append(

            build_metadata(

                image,

                page_text

            )

        )

    return metadata
# --------------------------------------------------
# Stage 9.3
# Metadata Normalizer
# --------------------------------------------------


def normalize_metadata(image):

    image.normalized_metadata = {

        "page": int(getattr(image, "page_no", 0)),

        "layout": getattr(
            image,
            "layout_type",
            "unknown"
        ),

        "orientation": getattr(
            image,
            "orientation",
            "unknown"
        ),

        "resolution":

            f"{getattr(image,'width',0)}x{getattr(image,'height',0)}",

        "aspect_ratio":

            round(
                float(
                    getattr(image, "aspect_ratio", 0)
                ),
                3
            ),

        "file_size":

            int(
                getattr(image, "file_size", 0)
            ),

        "metadata_score":

            round(
                float(
                    getattr(image, "metadata_score", 0)
                ),
                3
            ),

        "quality_score":

            round(
                float(
                    getattr(image, "quality_score", 0)
                ),
                3
            ),

        "ocr_score":

            round(
                float(
                    getattr(image, "ocr_score", 0)
                ),
                3
            ),

        "layout_score":

            round(
                float(
                    getattr(image, "layout_score", 0)
                ),
                3
            ),

        "vision_score":

            round(
                float(
                    getattr(image, "vision_score", 0)
                ),
                3
            ),

        "decision":

            getattr(
                image,
                "final_decision",
                "REVIEW"
            )

    }

    return image


# --------------------------------------------------
# Batch
# --------------------------------------------------

def normalize_all_metadata(images):

    print("\n==============================")
    print("STAGE 9.3 : METADATA NORMALIZER")
    print("==============================")

    for image in images:

        normalize_metadata(image)

    print(f"Normalized : {len(images)}")

    print("\nSamples\n")

    for image in images[:5]:

        print(image.normalized_metadata)

        print()

    return images
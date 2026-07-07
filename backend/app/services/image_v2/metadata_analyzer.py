import os


def analyze_metadata(images, page_lookup):
    """
    Stage 1
    Image Metadata Analyzer

    Computes basic metadata for every extracted image.
    No filtering is performed here.
    """

    print("\n==============================")
    print("IMAGE METADATA ANALYZER")
    print("==============================")

    for image in images:

        ##################################################
        # Resolution
        ##################################################

        image.resolution = (
            image.width,
            image.height
        )

        ##################################################
        # Aspect Ratio
        ##################################################

        if image.height > 0:

            image.aspect_ratio = round(
                image.width / image.height,
                3
            )

        else:

            image.aspect_ratio = 0.0

        ##################################################
        # Orientation
        ##################################################

        if image.width > image.height:

            image.orientation = "landscape"

        elif image.height > image.width:

            image.orientation = "portrait"

        else:

            image.orientation = "square"

        ##################################################
        # File Size
        ##################################################

        try:

            image.file_size = os.path.getsize(
                image.path
            )

        except Exception:

            image.file_size = 0

        ##################################################
        # Page Ratio
        ##################################################
        image.page_ratio = 0.0

    print(f"Metadata computed for {len(images)} images")
    print("\nSample Metadata")

    for image in images[:5]:

        print(

        f"Page {image.page_no} | "

        f"{image.width}x{image.height} | "

        f"Aspect={image.aspect_ratio:.2f} | "

        f"PageRatio={image.page_ratio:.3f} | "

        f"{image.orientation} | "

        f"{image.file_size} bytes"

    )

    return images
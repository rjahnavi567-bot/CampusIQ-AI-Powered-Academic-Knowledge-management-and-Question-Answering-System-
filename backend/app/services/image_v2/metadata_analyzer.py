import os


def analyze_metadata(images, page_lookup):
    """
    Stage 1
    Metadata Analyzer

    Computes metadata required by all later scoring stages.
    """

    print("\n==============================")
    print("IMAGE METADATA ANALYZER")
    print("==============================")

    for image in images:

        ####################################################
        # Resolution
        ####################################################

        image.resolution = (image.width, image.height)

        ####################################################
        # Image Area
        ####################################################

        image.area = image.width * image.height

        ####################################################
        # Aspect Ratio
        ####################################################

        if image.height > 0:
            image.aspect_ratio = round(
                image.width / image.height,
                3
            )
        else:
            image.aspect_ratio = 0.0

        ####################################################
        # Orientation
        ####################################################

        if image.width > image.height:
            image.orientation = "landscape"

        elif image.height > image.width:
            image.orientation = "portrait"

        else:
            image.orientation = "square"

        ####################################################
        # File Size
        ####################################################

        try:
            image.file_size = os.path.getsize(image.path)

        except Exception:
            image.file_size = 0

        ####################################################
        # Page Information
        ####################################################

        page = page_lookup.get(image.page_no)

        if page is not None:

            page_width = page["width"]
            page_height = page["height"]

        else:

            page_width = image.width
            page_height = image.height

        image.page_width = page_width
        image.page_height = page_height

        ####################################################
        # Page Area
        ####################################################

        image.page_area = page_width * page_height

        ####################################################
        # Page Ratio
        ####################################################

        if image.page_area > 0:

            image.page_ratio = round(

                image.area /

                image.page_area,

                4

            )

        else:

            image.page_ratio = 0.0

    ####################################################
    # Summary
    ####################################################

    print(f"Metadata computed for {len(images)} images")

    print("\nSample Metadata\n")

    for image in images[:10]:

        print(

            f"Page {image.page_no:3} | "

            f"{image.width}x{image.height} | "

            f"Area={image.area} | "

            f"PageRatio={image.page_ratio:.4f} | "

            f"{image.orientation:9} | "

            f"{image.file_size} bytes"

        )

    return images
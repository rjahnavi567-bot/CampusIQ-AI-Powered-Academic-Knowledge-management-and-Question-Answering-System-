import os
import cv2


def create_debug_folder(output_dir):

    debug_dir = os.path.join(
        output_dir,
        "debug"
    )

    os.makedirs(
        debug_dir,
        exist_ok=True
    )

    return debug_dir


def save_debug_image(

    image,

    output_dir,

    page_no,

    stage

):
    """
    Save one debug image.

    Example:

    page_1_render.png
    page_1_layout.png
    page_1_regions.png
    page_1_fusion.png
    """

    debug_dir = create_debug_folder(
        output_dir
    )

    filename = os.path.join(

        debug_dir,

        f"page_{page_no}_{stage}.png"

    )

    cv2.imwrite(

        filename,

        image,

        [cv2.IMWRITE_PNG_COMPRESSION, 0]

    )

    return filename


def save_render(
    page_image,
    output_dir,
    page_no
):

    return save_debug_image(

        page_image,

        output_dir,

        page_no,

        "render"

    )


def save_layout(
    image,
    output_dir,
    page_no
):

    return save_debug_image(

        image,

        output_dir,

        page_no,

        "layout"

    )


def save_regions(
    image,
    output_dir,
    page_no
):

    return save_debug_image(

        image,

        output_dir,

        page_no,

        "regions"

    )


def save_fusion(
    image,
    output_dir,
    page_no
):

    return save_debug_image(

        image,

        output_dir,

        page_no,

        "fusion"

    )
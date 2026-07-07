import os
import cv2


def save_crop(
    crop,
    output_dir,
    page_no,
    index
):
    """
    Save crop without changing quality.
    """

    if crop is None:
        return None

    if crop.size == 0:
        return None

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    filename = os.path.join(

        output_dir,

        f"page_{page_no}_figure_{index}.png"

    )

    success = cv2.imwrite(

        filename,

        crop,

        [
            cv2.IMWRITE_PNG_COMPRESSION,
            0
        ]

    )

    if not success:
        return None

    return filename
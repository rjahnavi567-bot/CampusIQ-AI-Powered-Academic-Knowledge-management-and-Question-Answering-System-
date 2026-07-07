import fitz
import cv2
import numpy as np

RENDER_SCALE = 3.0


def render_page(page):
    """
    Render a single PDF page into a high-quality BGR image.
    """

    pix = page.get_pixmap(
        matrix=fitz.Matrix(
            RENDER_SCALE,
            RENDER_SCALE
        ),
        alpha=False
    )

    image = np.frombuffer(
        pix.samples,
        dtype=np.uint8
    ).reshape(
        pix.height,
        pix.width,
        pix.n
    )

    # PyMuPDF returns RGB
    if pix.n == 3:

        image = cv2.cvtColor(
            image,
            cv2.COLOR_RGB2BGR
        )

    elif pix.n == 4:

        image = cv2.cvtColor(
            image,
            cv2.COLOR_RGBA2BGR
        )

    return image
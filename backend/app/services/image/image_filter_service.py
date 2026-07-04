import cv2
import hashlib
import numpy as np
import re

def clean_filename(name):

    name = name.lower()

    name = re.sub(r"[^a-z0-9 ]", "", name)

    name = name.replace(" ", "_")

    while "__" in name:
        name = name.replace("__", "_")

    return name[:80]


def generate_image_hash(image_path):

    sha = hashlib.sha256()

    with open(image_path, "rb") as f:

        while True:

            data = f.read(8192)

            if not data:
                break

            sha.update(data)

    return sha.hexdigest()[:8]




def is_useful_image(image_path):

    image = cv2.imread(image_path)

    if image is None:
        return False

    h, w = image.shape[:2]

    # Too small
    if w < 180 or h < 180:
        return False

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Blank image

    std = np.std(gray)

    if std < 8:
        return False

    # Edge Density

    edges = cv2.Canny(gray, 80, 180)

    edge_ratio = cv2.countNonZero(edges) / (w * h)

    if edge_ratio < 0.01:
        return False

    if edge_ratio > 0.42:
        return False

    # White ratio

    white_ratio = np.sum(gray > 245) / (w * h)

    if white_ratio > 0.97:
        return False

    return True
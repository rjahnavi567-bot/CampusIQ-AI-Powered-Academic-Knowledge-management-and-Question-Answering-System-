import os
import hashlib


def remove_duplicate_images(images):

    unique = []
    hashes = set()

    for image in images:

        try:

            with open(image["path"], "rb") as f:
                h = hashlib.md5(f.read()).hexdigest()

            if h in hashes:
                os.remove(image["path"])
                continue

            hashes.add(h)
            unique.append(image)

        except Exception:
            unique.append(image)

    return unique
def is_duplicate(processed, image):

    for old in processed:

        # Only exact duplicate images
        if old.get("image_hash") == image.get("image_hash"):

            print(
                f"Duplicate removed (hash): {image['path']}"
            )

            return True

    return False
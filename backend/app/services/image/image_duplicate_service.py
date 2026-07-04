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

        same_title = (
            old["title"].lower().strip()
            ==
            image["title"].lower().strip()
        )

        same_hash = (
            old["image_hash"]
            ==
            image["image_hash"]
        )

        if same_hash:
            return True

        if (
            same_title
            and
            abs(old["page_no"] - image["page_no"]) <= 1
        ):
            return True

    return False
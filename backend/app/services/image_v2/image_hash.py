import hashlib


# --------------------------------------------------
# Compute MD5 Hash
# --------------------------------------------------

def compute_md5(image_path):

    md5 = hashlib.md5()

    with open(image_path, "rb") as f:

        while True:

            chunk = f.read(8192)

            if not chunk:
                break

            md5.update(chunk)

    return md5.hexdigest()
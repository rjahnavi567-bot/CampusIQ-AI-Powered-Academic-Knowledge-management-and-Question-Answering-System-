import os
import hashlib
import re
import glob
import cv2
import numpy as np
from app.services.image_extraction_service import (
    extract_pdf_images,
    extract_docx_images,
    extract_pptx_images,
    extract_image_file,
    extract_images
)

from app.services.image_understanding_service import (
    understand_image
)

from app.services.groq_vision_service import (
    analyze_image
)

from app.services.image_embedding_service import (
    embed_image
)

from app.services.image_context_service import (
    get_page_text
)
from app.services.diagram_title_service import (
    generate_diagram_title
)

# ---------------------------------------------------------
# Duplicate Removal
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# Image Processing Pipeline
# ---------------------------------------------------------

def process_images(
    file_path,
    document_id,
    pages,
    source_file
):

    extension = os.path.splitext(
        file_path
    )[1].lower()

    page_lookup = {

        page["page_no"]: page["text"]

        for page in pages

    }

    # -----------------------------------------------------
    # Extract Images
    # -----------------------------------------------------

    if extension == ".pdf":

        images = extract_pdf_images(
            file_path,
            document_id
        )

    elif extension == ".docx":

        images = extract_docx_images(
            file_path,
            document_id
        )

    elif extension == ".pptx":

        images = extract_pptx_images(
            file_path,
            document_id
        )

    elif extension in [

        ".png",

        ".jpg",

        ".jpeg"

    ]:

        images = extract_image_file(
            file_path
        )

    else:

        images = extract_images(
            file_path,
            document_id
        )

    # -----------------------------------------------------
    # Remove duplicates
    # -----------------------------------------------------

    images = remove_duplicate_images(images)

    print()

    print("Unique Images :", len(images))

    print()

    # -----------------------------------------------------
    # Understand every image
    # -----------------------------------------------------

    processed = []

    for image in images:

        if not os.path.exists(image["path"]):

            continue

        # Ignore useless images

        if not is_useful_image(image["path"]):

          try:
             os.remove(image["path"])
          except:
             pass

          continue

        understanding = understand_image(

            image["path"]

        )
        caption = understanding["caption"].lower()

        reject_words = [

    "page of text",

    "text document",

    "paragraph",

    "printed text",

    "book page",

    "document page",

    "page containing text",

    "scanned page",

    "screenshot",

    "website",

    "article",

    "newspaper",

    "person",

    "people",

    "portrait",

    "face",

    "logo",

    "icon",

    "animal",

    "tree",

    "building",

    "landscape"

]

        caption = understanding["caption"].lower()

        if any(word in caption for word in reject_words):

            try:
                os.remove(image["path"])
            except:
                pass

            continue

        image["caption"] = understanding["caption"]

        image["ocr_text"] = understanding["ocr_text"]
        ocr_words = len(image["ocr_text"].split())

        if ocr_words > 120:

            try:
                os.remove(image["path"])
            except:
                pass

            continue

        # -----------------------------------
        # Academic Diagram Title
        # -----------------------------------

        image["title"] = generate_diagram_title(

    image["caption"],

    image["ocr_text"]

)

        try:

            image["vision"] = analyze_image(

                image["path"]

            )

        except Exception:

            image["vision"] = ""

        image["page_text"] = get_page_text(

            page_lookup,

            image["page_no"]

        )

        image["source_file"] = source_file

        image["file_type"] = os.path.splitext(

            source_file

        )[1].lower()

        image["document_id"] = document_id
        # -----------------------------------
        # Rename image using title + page + hash
        # -----------------------------------

        image_hash = generate_image_hash(image["path"])

        image["image_hash"] = image_hash

        safe_title = clean_filename(image["title"])

        extension = os.path.splitext(image["path"])[1]
        folder = os.path.dirname(image["path"])

        base = (
    f"{document_id}_"
    f"{safe_title}"
    f"_page{image['page_no']}"
    f"_{image_hash}"
)

        new_path = os.path.join(
    folder,
    base + extension
)

        counter = 1

        while os.path.exists(new_path):

            new_path = os.path.join(

        folder,

        f"{base}_{counter}{extension}"

    )

            counter += 1
        try:

            if image["path"] != new_path:

                if os.path.exists(new_path):

                    base = os.path.splitext(new_name)[0]

                    new_name = (
                f"{base}_{image_hash[:4]}"
                f"{extension}"
            )

                    new_path = os.path.join(
                os.path.dirname(image["path"]),
                new_name
            )

                os.rename(
            image["path"],
            new_path
        )

                image["path"] = new_path

        except Exception as e:

            print("Rename Error:", e)

        # -----------------------------------------
        # CLIP Embedding
        # -----------------------------------------

        try:

            image["clip_embedding"] = embed_image(

                image["path"]

            )

        except Exception:

            image["clip_embedding"] = None
        
        duplicate = False

        for old in processed:

            same_title = (

    old["title"].lower().strip()

    == image["title"].lower().strip()

)

            same_hash = (

    old.get("image_hash")

    == image.get("image_hash")

)

            if same_hash or (

    same_title

    and

    abs(

        old["page_no"]

        - image["page_no"]

    ) <= 1

):

                duplicate = True
                break

        if duplicate:

            try:
                os.remove(image["path"])
            except:
                pass

            continue

        if image.get("image_hash"):

            processed.append(image)
  

    page_images = glob.glob(
    f"uploads/images/{document_id}/page_*.png"
)

    for img in page_images:
      if os.path.exists(img):

        try:
           os.remove(img)
        except:
           pass

    return processed

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
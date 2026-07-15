from PIL import Image


def load_pages(file_path):

    image = Image.open(file_path).convert("RGB")

    return [

        {

            "page_no": 1,

            "image": image

        }

    ]
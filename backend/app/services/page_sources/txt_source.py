from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


PAGE_WIDTH = 1654
PAGE_HEIGHT = 2339

MARGIN = 80
LINE_HEIGHT = 40


def load_pages(file_path):

    try:
        font = ImageFont.truetype("arial.ttf", 26)
    except:
        font = ImageFont.load_default()

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.readlines()

    pages = []

    image = Image.new(
        "RGB",
        (PAGE_WIDTH, PAGE_HEIGHT),
        "white"
    )

    draw = ImageDraw.Draw(image)

    y = MARGIN
    page_no = 1

    for line in text:

        draw.text(
            (MARGIN, y),
            line.strip(),
            fill="black",
            font=font
        )

        y += LINE_HEIGHT

        if y > PAGE_HEIGHT - MARGIN:

            pages.append({
                "page_no": page_no,
                "image": image
            })

            page_no += 1

            image = Image.new(
                "RGB",
                (PAGE_WIDTH, PAGE_HEIGHT),
                "white"
            )

            draw = ImageDraw.Draw(image)

            y = MARGIN

    pages.append({
        "page_no": page_no,
        "image": image
    })

    return pages
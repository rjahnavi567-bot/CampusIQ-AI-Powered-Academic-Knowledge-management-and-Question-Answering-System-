import io

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# ==========================================================
# Loader
# ==========================================================

def load_pages(file_path):

    source = DocxSource(file_path)

    images = source.render_pages()

    pages = []

    for i, img in enumerate(images):

        pages.append({

            "page_no": i + 1,

            "image": img

        })

    return pages

# ==========================================================
# Iterate through document while preserving order
# ==========================================================

def iter_block_items(parent):

    parent_elm = parent.element.body

    for child in parent_elm.iterchildren():

        if isinstance(child, CT_P):
            yield Paragraph(child, parent)

        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


# ==========================================================
# DOCX SOURCE
# ==========================================================

class DocxSource:

    PAGE_WIDTH = 1654
    PAGE_HEIGHT = 2339

    MARGIN_X = 80
    MARGIN_Y = 80

    LINE_HEIGHT = 40

    MAX_IMAGE_WIDTH = 900

    def __init__(self, docx_path):

        self.docx_path = docx_path

    # ------------------------------------------------------

    def _new_page(self):

        image = Image.new(

            "RGB",

            (self.PAGE_WIDTH, self.PAGE_HEIGHT),

            "white"

        )

        draw = ImageDraw.Draw(image)

        return image, draw

    # ------------------------------------------------------

    def render_pages(self):

        document = Document(self.docx_path)

        try:

            font = ImageFont.truetype("arial.ttf", 26)

        except Exception:

            font = ImageFont.load_default()

        pages = []

        image, draw = self._new_page()

        y = self.MARGIN_Y

        # ==================================================
        # Walk document
        # ==================================================

        for block in iter_block_items(document):

            # =============================================
            # PARAGRAPH
            # =============================================

            if isinstance(block, Paragraph):

                text = block.text.strip()

                if text:

                    draw.text(

                        (self.MARGIN_X, y),

                        text,

                        fill="black",

                        font=font

                    )

                    y += self.LINE_HEIGHT

                # ------------------------------------------
                # Embedded Images
                # ------------------------------------------

                for run in block.runs:

                    try:

                        blips = run._element.xpath(".//a:blip")

                        if len(blips) == 0:
                            continue

                        rid = blips[0].get(

                            "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"

                        )

                        image_part = document.part.related_parts[rid]

                        picture = Image.open(

                            io.BytesIO(image_part.blob)

                        ).convert("RGB")

                        # resize

                        if picture.width > self.MAX_IMAGE_WIDTH:

                            scale = self.MAX_IMAGE_WIDTH / picture.width

                            picture = picture.resize(

                                (

                                    self.MAX_IMAGE_WIDTH,

                                    int(picture.height * scale)

                                )

                            )

                        # new page if required

                        if y + picture.height > self.PAGE_HEIGHT - self.MARGIN_Y:

                            pages.append(image)

                            image, draw = self._new_page()

                            y = self.MARGIN_Y

                        image.paste(

                            picture,

                            (

                                self.MARGIN_X,

                                y

                            )

                        )

                        y += picture.height + 30

                    except Exception:

                        continue

            # =============================================
            # TABLE
            # =============================================

            elif isinstance(block, Table):

                if y + 220 > self.PAGE_HEIGHT - self.MARGIN_Y:

                    pages.append(image)

                    image, draw = self._new_page()

                    y = self.MARGIN_Y

                draw.rectangle(

                    (

                        self.MARGIN_X,

                        y,

                        self.MARGIN_X + 600,

                        y + 180

                    ),

                    outline="black",

                    width=2

                )

                draw.text(

                    (

                        self.MARGIN_X + 20,

                        y + 20

                    ),

                    "[TABLE]",

                    fill="black",

                    font=font

                )

                y += 220

            # =============================================
            # New Page
            # =============================================

            if y > self.PAGE_HEIGHT - self.MARGIN_Y:

                pages.append(image)

                image, draw = self._new_page()

                y = self.MARGIN_Y

        pages.append(image)

        return pages
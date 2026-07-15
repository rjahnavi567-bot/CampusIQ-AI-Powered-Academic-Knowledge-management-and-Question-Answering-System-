import fitz

from app.services.image_v2.page_renderer import render_page


def load_pages(file_path):

    pdf = fitz.open(file_path)

    pages = []

    for i in range(len(pdf)):

        page = pdf.load_page(i)

        page_image = render_page(page)

        pages.append(

            {
                "page_no": i + 1,
                "image": page_image
            }

        )

    pdf.close()

    return pages
import os

from .pdf_source import load_pages as load_pdf
from .docx_source import load_pages as load_docx
from .ppt_source import load_pages as load_ppt
from .txt_source import load_pages as load_txt
from .image_source import load_pages as load_image


def load_document(file_path):

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return load_pdf(file_path)

    elif ext == ".docx":
        return load_docx(file_path)

    elif ext == ".pptx":
        return load_ppt(file_path)

    elif ext == ".txt":
        return load_txt(file_path)

    elif ext in [".png", ".jpg", ".jpeg"]:
        return load_image(file_path)

    else:
        raise Exception(f"Unsupported file: {ext}")
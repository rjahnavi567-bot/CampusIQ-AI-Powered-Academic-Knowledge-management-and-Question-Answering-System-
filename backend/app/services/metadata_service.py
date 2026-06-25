import fitz
from docx import Document
from pptx import Presentation


def extract_metadata(file_path):

    metadata = {

        "title": "",
        "author": "",
        "subject": ""

    }

    try:

        if file_path.endswith(".pdf"):

            pdf = fitz.open(file_path)

            meta = pdf.metadata

            metadata["title"] = (
                meta.get("title", "")
            )

            metadata["author"] = (
                meta.get("author", "")
            )

            metadata["subject"] = (
                meta.get("subject", "")
            )

        elif file_path.endswith(".docx"):

            doc = Document(file_path)

            props = doc.core_properties

            metadata["title"] = (
                props.title or ""
            )

            metadata["author"] = (
                props.author or ""
            )

            metadata["subject"] = (
                props.subject or ""
            )

        elif file_path.endswith(".pptx"):

            ppt = Presentation(file_path)

            props = ppt.core_properties

            metadata["title"] = (
                props.title or ""
            )

            metadata["author"] = (
                props.author or ""
            )

            metadata["subject"] = (
                props.subject or ""
            )

    except Exception as e:

        print("Metadata Error:", e)

    return metadata
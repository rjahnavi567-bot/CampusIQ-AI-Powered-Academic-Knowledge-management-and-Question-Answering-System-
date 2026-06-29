from app.database.models import Document


def create_document(
    db,
    filename,
    file_path,
    file_hash
):
    """
    Creates initial database entry.
    """

    new_doc = Document(

        filename=filename,

        file_path=file_path,

        subject="General",

        unit="Unit-1",

        uploaded_by=1,

        status="Processing",

        chunk_count=0,

        file_hash=file_hash,

        content_signature="",

        embedding=""
    )

    db.add(new_doc)

    db.commit()

    db.refresh(new_doc)

    return new_doc


def update_document_filename(
    db,
    document,
    new_filename,
    new_path
):
    """
    Update filename after smart title generation.
    """

    document.filename = new_filename

    document.file_path = new_path

    db.commit()


def finalize_document(
    db,
    document,
    chunk_count
):
    """
    Mark upload complete.
    """

    document.chunk_count = chunk_count

    document.status = "Processed"

    db.commit()
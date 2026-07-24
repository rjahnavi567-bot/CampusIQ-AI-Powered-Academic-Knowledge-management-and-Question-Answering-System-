from app.database.models import Document


def create_document(
    db,
    filename,
    file_path,
    file_hash,
    uploaded_by
):
    """
    Create document WITHOUT committing.
    """

    new_doc = Document(

        filename=filename,

        file_path=file_path,

        subject="General",

        unit="Unit-1",

        uploaded_by=uploaded_by,

        status="Processing",

        chunk_count=0,

        file_hash=file_hash,

        content_signature="",

        embedding=""

    )

    db.add(new_doc)

    # Flush sends INSERT to DB
    # but DOES NOT commit transaction
    db.flush()

    # Primary key becomes available
    db.refresh(new_doc)

    return new_doc


def update_document_filename(
    db,
    document,
    new_filename,
    new_path
):
    """
    Update filename.
    No commit here.
    """

    document.filename = new_filename
    document.file_path = new_path


def finalize_document(
    db,
    document,
    chunk_count
):
    """
    Mark upload complete.
    No commit here.
    """

    document.chunk_count = chunk_count
    document.status = "Processed"
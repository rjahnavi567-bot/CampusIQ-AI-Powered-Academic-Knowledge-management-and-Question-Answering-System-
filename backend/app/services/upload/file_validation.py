import os
from fastapi import UploadFile

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".pptx",
    ".txt",
    ".jpg",
    ".jpeg",
    ".png"
}

# 50 MB
MAX_FILE_SIZE = 50 * 1024 * 1024


def validate_file(file: UploadFile):
    """
    Validates uploaded file type and size.

    Returns:
        {
            "valid": True
        }

    or

        {
            "valid": False,
            "message": "..."
        }
    """

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        return {
            "valid": False,
            "message": f"Unsupported file type: {extension}"
        }

    # Get file size
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        return {
            "valid": False,
            "message": "File size exceeds 50 MB limit."
        }

    return {
        "valid": True
    }
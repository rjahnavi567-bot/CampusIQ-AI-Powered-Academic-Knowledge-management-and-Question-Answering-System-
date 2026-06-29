def build_upload_response(
    original_filename,
    stored_filename,
    suggested_title,
    chunks,
    images,
    similarity_warning
):
    """
    Builds upload response.
    """

    response = {

        "message":
        "File processed successfully",

        "original_filename":
        original_filename,

        "stored_filename":
        stored_filename,

        "suggested_title":
        suggested_title,

        "chunks_created":
        len(chunks),

        "images_extracted":
        len(images),

        "images_understood":
        len(images)
    }

    if similarity_warning:

        response["warning"] = (
            "Similar document exists"
        )

        response["similarity"] = (
            similarity_warning["similarity"]
        )

        response["existing_document"] = (
            similarity_warning["existing_document"]
        )

    return response
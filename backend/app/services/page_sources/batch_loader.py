from .source_loader import load_document


def load_document_batches(file_path, batch_size=5):
    """
    Yield pages in small batches.

    Example:
        pages 1-5
        pages 6-10
        pages 11-15
    """

    pages = load_document(file_path)

    total = len(pages)

    for i in range(0, total, batch_size):

        yield pages[i:i + batch_size]
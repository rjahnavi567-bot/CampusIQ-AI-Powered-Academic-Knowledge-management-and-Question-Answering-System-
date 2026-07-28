from app.database.connection import SessionLocal
from app.database.models import Document
from app.services.trie_service import document_trie
from app.services.trie_service import (
    document_trie,
    TrieNode
)
class DocumentCache:

    def __init__(self):

        self.cache = {}

    # -----------------------------
    # Load every document once
    # -----------------------------
    def load_cache(self):

        db = SessionLocal()

        try:

            documents = db.query(Document).all()

            self.cache.clear()
            document_trie.root = TrieNode()

            for doc in documents:

                self.cache[doc.filename.lower()] = doc
                document_trie.insert(doc.filename)

            print(
                f"Document Cache Loaded : {len(self.cache)} documents"
            )

        finally:

            db.close()

    # -----------------------------
    # Add document
    # -----------------------------
    def add_document(self, document):

        self.cache[
        document.filename.lower()
    ] = document

        document_trie.insert(
        document.filename
    )

        print(
        f"Added to Cache : {document.filename}"
    )
    # -----------------------------
    # Remove document
    # -----------------------------
    def remove_document(self, filename):

        self.cache.pop(
            filename.lower(),
            None
        )
        document_trie.delete(
        filename
    )

        print(
            f"Removed from Cache : {filename}"
        )

    # -----------------------------
    # Exact Search
    # -----------------------------
    def get_document(self, filename):

        return self.cache.get(
            filename.lower()
        )

    # -----------------------------
    # Exists
    # -----------------------------
    def exists(self, filename):

        return (
            filename.lower()
            in self.cache
        )

    # -----------------------------
    # Number of Cached Documents
    # -----------------------------
    def size(self):

        return len(self.cache)


document_cache = DocumentCache()
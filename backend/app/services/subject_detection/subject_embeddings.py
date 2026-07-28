import json

from app.database.connection import SessionLocal
from app.database.models import Subject

from app.services.embedding_service import model


class SubjectEmbeddingGenerator:

    def generate_embeddings(self):

        db = SessionLocal()

        try:

            subjects = db.query(Subject).all()

            print(
                f"Generating embeddings for {len(subjects)} subjects..."
            )

            for subject in subjects:

                text = (
                    subject.name +
                    ". " +
                    subject.description
                )

                embedding = model.encode(
    text,
    normalize_embeddings=True
)

                subject.embedding = json.dumps(
                    embedding.tolist()
                )

            db.commit()

            print("Subject embeddings generated.")

        finally:

            db.close()


generator = SubjectEmbeddingGenerator()
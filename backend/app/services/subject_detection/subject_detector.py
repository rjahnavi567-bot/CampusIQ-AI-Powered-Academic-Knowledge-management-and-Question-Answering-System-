import json
import numpy as np

from app.database.connection import SessionLocal
from app.database.models import AcademicSubject
from app.services.embedding_service import model


class SubjectDetector:

    def detect_subject(self, text):

        db = SessionLocal()

        try:

            document_embedding = model.encode(
                text,
                normalize_embeddings=True
            )

            subjects = db.query(
                AcademicSubject
            ).all()

            similarities = []

            for subject in subjects:

                if not subject.embedding:
                    continue

                subject_embedding = np.array(
                    json.loads(subject.embedding)
                )

                score = float(
                    np.dot(
                        document_embedding,
                        subject_embedding
                    )
                )

                similarities.append({

                    "subject": subject.subject_name,

                    "score": round(score, 4)

                })

            similarities.sort(

                key=lambda x: x["score"],

                reverse=True

            )

            return {
    "top_matches": similarities
}

        finally:

            db.close()


subject_detector = SubjectDetector()


def detect_subject(text):

    return subject_detector.detect_subject(text)
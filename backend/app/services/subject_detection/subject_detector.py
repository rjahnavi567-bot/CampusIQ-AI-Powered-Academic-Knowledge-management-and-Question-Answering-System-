import json
import numpy as np

from app.database.connection import SessionLocal
from app.database.models import Subject

from app.services.embedding_service import model


class SubjectDetector:

    def detect_subject(self, text):

        db = SessionLocal()

        try:

            # Generate embedding for uploaded document
            document_embedding = model.encode(
                text,
                normalize_embeddings=True
            )

            subjects = db.query(Subject).all()

            best_subject = None
            best_score = -1

            for subject in subjects:

                if not subject.embedding:
                    continue

                subject_embedding = np.array(
                    json.loads(subject.embedding)
                )

                score = np.dot(
                    document_embedding,
                    subject_embedding
                )

                if score > best_score:

                    best_score = score
                    best_subject = subject

            return {

                "subject": best_subject.name if best_subject else None,

                "score": round(
                    float(best_score),
                    4
                )

            }

        finally:

            db.close()


subject_detector = SubjectDetector()
def detect_subject(text):
    return subject_detector.detect_subject(text)
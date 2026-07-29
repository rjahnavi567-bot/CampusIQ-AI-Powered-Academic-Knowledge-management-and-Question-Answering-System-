import json
import numpy as np

from app.database.connection import SessionLocal
from app.database.models import AcademicSubject

from app.services.embedding_service import model


class SubjectDetector:

  def detect_subject(self, text):

    db = SessionLocal()

    try:

        # Generate document embedding
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

            similarity = float(
                np.dot(
                    document_embedding,
                    subject_embedding
                )
            )

            similarities.append({

                "subject": subject.subject_name,

                "score": similarity

            })

        similarities.sort(

            key=lambda x: x["score"],

            reverse=True

        )

        if len(similarities) == 0:

            return {

                "primary_subject": None,

                "confidence": 0,

                "secondary_subjects": []

            }

        primary = similarities[0]

        secondary = []

        for item in similarities[1:]:

            if item["score"] >= 0.75:

                secondary.append(
                    item["subject"]
                )

        return {

            "primary_subject":
            primary["subject"],

            "confidence":
            round(
                primary["score"] * 100,
                2
            ),

            "secondary_subjects":
            secondary

        }

    finally:

        db.close()

subject_detector = SubjectDetector()
def detect_subject(text):
    return subject_detector.detect_subject(text)
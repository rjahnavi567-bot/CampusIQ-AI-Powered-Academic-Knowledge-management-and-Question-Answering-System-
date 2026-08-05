import json
import numpy as np

from app.services.embedding_service import model

from app.services.subject_detection.subject_repository import (
    load_all_subjects
)


class SubjectDetector:

    def compare_against_subjects(
        self,
        document_embedding,
        subjects
    ):

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

                "parent_subject": subject.parent_subject,

                "branch": subject.branch,

                "score": round(score, 4)

            })

        similarities.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return similarities

    def detect_subject(self, text):

        document_embedding = model.encode(
            text,
            normalize_embeddings=True
        )

        ##################################################
        # Compare against ALL subjects
        ##################################################

        subjects = load_all_subjects()

        matches = self.compare_against_subjects(

            document_embedding,

            subjects

        )

        ##################################################
        # Return Top 10 matches
        ##################################################

        return {

            "top_matches": matches[:10]

        }


subject_detector = SubjectDetector()


def detect_subject(text):

    return subject_detector.detect_subject(text)
import json

from app.database.connection import SessionLocal
from app.database.models import AcademicSubject

from app.services.embedding_service import (
    create_embedding
)


def generate_subject_embeddings():

    db = SessionLocal()

    try:

        subjects = (
            db.query(AcademicSubject)
            .all()
        )


        for subject in subjects:

            if subject.embedding:
                print(
                    f"Skipping {subject.subject_name}"
                )
                continue


            text = f"""
Subject

{subject.subject_name}

Parent Subject

{subject.parent_subject}

Description

{subject.description}

Keywords

{subject.keywords}

Topics

{subject.topics}
"""


            embedding = create_embedding(
                text
            )


            subject.embedding = json.dumps(
                embedding
            )


            print(
                "Generated:",
                subject.subject_name
            )


        db.commit()

        print(
            "All subject embeddings generated."
        )


    finally:

        db.close()



if __name__ == "__main__":

    generate_subject_embeddings()
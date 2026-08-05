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
            parts = []

            parts.append(subject.subject_name)

            if subject.parent_subject:
                parts.append(subject.parent_subject)

            if subject.aliases:
                parts.append(subject.aliases)

            if subject.description:
                parts.append(subject.description)

            if subject.keywords:
                parts.append(subject.keywords)

            if subject.topics:
                parts.append(subject.topics)

            text = "\n".join(parts)


            text = f"""
Subject:
{subject.subject_name}

Parent Subject:
{subject.parent_subject}

Description:
{subject.description}

Keywords:
{subject.keywords}

Topics:
{subject.topics}

Aliases:
{subject.aliases}
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
import json

from app.database.connection import SessionLocal
from app.database.models import AcademicSubject

db = SessionLocal()

with open(
    "app/data/academic_subjects.json",
    "r",
    encoding="utf-8"
) as f:

    subjects = json.load(f)

try:

    db.query(AcademicSubject).delete()

    db.commit()

    for item in subjects:

        db_subject = AcademicSubject(

            subject_name=item["subject_name"],

            parent_subject=item["parent_subject"],

            description=item["description"],

            keywords=",".join(item["keywords"]),

            topics=",".join(item["topics"])

        )

        db.add(db_subject)

    db.commit()

    print("Subjects inserted successfully.")

finally:

    db.close()
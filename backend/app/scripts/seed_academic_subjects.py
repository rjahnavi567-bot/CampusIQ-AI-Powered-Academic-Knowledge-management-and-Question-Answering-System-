import json

from app.database.connection import SessionLocal
from app.database.models import AcademicSubject

db = SessionLocal()

with open(
    "app/scripts/common_subjects.json",
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

    branch=item["branch"],

    description=item.get("description", ""),

    keywords=",".join(item.get("keywords", [])),

    topics=",".join(item.get("topics", [])),

    aliases=",".join(item.get("aliases", []))

)

        db.add(db_subject)

    db.commit()

    print("Academic subjects inserted successfully.")

finally:

    db.close()
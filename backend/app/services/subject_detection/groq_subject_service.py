from groq import Groq
import json
from app.services.groq_service import client
from app.database.connection import SessionLocal
from app.database.models import AcademicSubject


def classify_subject_with_groq(
    preview_text
):
    db = SessionLocal()

    subjects = db.query(
    AcademicSubject
).all()

    subject_information = ""

    for subject in subjects:

        subject_information += f"""
Subject:
{subject.subject_name}

Parent:
{subject.parent_subject}

Keywords:
{subject.keywords}

-------------------------------------
"""

    db.close()
    example = """
{
    "primary_subject":"Machine Learning",
    "parent_subject":"Artificial Intelligence",
    "confidence":96,
    "matched_keywords":[
        "classification",
        "supervised learning"
    ],
    "secondary_subjects":[
        "Artificial Intelligence"
    ]
}
"""

    prompt = f"""
You are an academic document classifier.

Your task is to classify the uploaded academic document.

Available Subjects

{subject_information}

Uploaded Document Preview

{preview_text}

Instructions

1. Read the preview carefully.
2. Compare with ALL available subjects.
3. Use keywords, concepts and terminology.
4. Choose the BEST matching subject.
5. If none match well, return General.
6. Confidence should be between 0 and 100.

Return ONLY valid JSON.

Example:

{example}
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {

                "role":"user",

                "content":prompt

            }

        ],

        temperature=0

    )
    content = response.choices[0].message.content

    content = (
    content
    .replace("```json", "")
    .replace("```", "")
    .strip()
)


    try:

        result = json.loads(content)

    except:

       result = {

    "primary_subject": None,

    "parent_subject": None,

    "confidence": 0,

    "matched_keywords": [],

    "secondary_subjects": [],

    "method": "groq"

}

    result["method"] = "groq"

    return result
import json

from app.services.groq_service import client


def classify_subject_with_groq(
    preview_text,
    candidates
):

    ####################################################
    # Build candidate list
    ####################################################

    subject_information = ""

    for item in candidates:

        subject_information += f"""
Subject:
{item['subject']}

Parent Subject:
{item['parent_subject']}

Embedding Score:
{item['score']}

-----------------------------------
"""

    ####################################################
    # Example JSON
    ####################################################

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
        "Deep Learning"
    ]
}
"""

    ####################################################
    # Prompt
    ####################################################

    prompt = f"""
You are an Academic Subject Classification Expert.

Your task is to classify an uploaded academic document.

The following subjects were retrieved using semantic embedding search.

Top Candidate Subjects

{subject_information}

Uploaded Document Preview

{preview_text}

Instructions

1. Read the preview carefully.

2. Compare ONLY with the candidate subjects above.

3. Do NOT invent a new subject.

4. Select the BEST matching subject from the list.

5. Use:
   - keywords
   - concepts
   - terminology
   - topics

6. Confidence must be between 0 and 100.

7. matched_keywords must contain only keywords actually found in the preview.

8. secondary_subjects should contain other closely related candidate subjects.

Return ONLY valid JSON.

Example

{example}
"""

    ####################################################
    # Call Groq
    ####################################################

    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0

    )

    ####################################################
    # Parse JSON
    ####################################################

    content = response.choices[0].message.content

    content = (
        content
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:

        result = json.loads(content)

    except Exception:

        result = {

            "primary_subject": None,

            "parent_subject": None,

            "confidence": 0,

            "matched_keywords": [],

            "secondary_subjects": []

        }

    ####################################################
    # Metadata
    ####################################################

    result["method"] = "groq"

    return result
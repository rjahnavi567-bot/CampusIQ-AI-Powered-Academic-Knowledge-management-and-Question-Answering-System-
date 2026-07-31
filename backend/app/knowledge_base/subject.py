def create_subject(
    subject_name,
    parent_subject,
    branches,
    description,
    keywords,
    topics,
    aliases=None
):
    return {
        "subject_name": subject_name,
        "parent_subject": parent_subject,
        "branches": branches,
        "description": description,
        "keywords": keywords,
        "topics": topics,
        "aliases": aliases or []
    }
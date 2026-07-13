import re


def clean_query(query: str):

    if query is None:
        return ""

    query = query.lower()

    query = re.sub(r"[^\w\s]", " ", query)

    query = re.sub(r"\s+", " ", query)

    return query.strip()
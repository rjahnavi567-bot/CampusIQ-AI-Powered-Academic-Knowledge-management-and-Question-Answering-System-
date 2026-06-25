from app.services.keyword_service import extract_keywords

text = """
Normalization reduces redundancy and improves
data integrity in relational databases.
"""

keywords = extract_keywords(text)

print(keywords)
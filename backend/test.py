from app.services.subject_detection.subject_classifier import classify_subject

text = """
Decision Tree Classification
Random Forest
Support Vector Machine
Regression
"""

print(classify_subject(text))
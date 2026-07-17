"""
DocLayout-YOLO wrapper.

Currently returns dummy predictions.

Later this file will call the real model.
"""


def classify_layout(image):

    return {

        "label": "Figure",

        "confidence": 1.0

    }
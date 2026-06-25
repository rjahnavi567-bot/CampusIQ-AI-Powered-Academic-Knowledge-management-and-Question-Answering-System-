import numpy as np


def cosine_similarity(
    embedding1,
    embedding2
):

    a = np.array(embedding1)

    b = np.array(embedding2)

    similarity = np.dot(a, b)

    return float(similarity)
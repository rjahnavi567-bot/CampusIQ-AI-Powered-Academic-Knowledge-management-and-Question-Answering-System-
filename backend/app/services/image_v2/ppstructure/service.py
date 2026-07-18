from .loader import get_engine


def analyze_layout(image_path):

    engine = get_engine()

    result = engine(image_path)

    return result
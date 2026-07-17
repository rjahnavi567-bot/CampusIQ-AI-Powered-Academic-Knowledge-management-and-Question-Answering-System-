"""
Loads DocLayout-YOLO model.

(Currently placeholder.)

Later this file will load the trained model.
"""


class LayoutModel:

    _instance = None

    def __init__(self):

        self.model = None

    @classmethod
    def get_model(cls):

        if cls._instance is None:

            cls._instance = LayoutModel()

        return cls._instance
from paddleocr import PPStructure

_ENGINE = None


def get_engine():
    global _ENGINE

    if _ENGINE is None:

        _ENGINE = PPStructure(
            show_log=False,
            layout=True,
            table=False,
            ocr=False
        )

    return _ENGINE
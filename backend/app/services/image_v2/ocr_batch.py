from concurrent.futures import ThreadPoolExecutor

from app.services.image_v2.ocr_service import extract_ocr


def process_ocr(images):

    def worker(img):

        img["ocr_text"] = extract_ocr(
            img["path"]
        )

        return img

    with ThreadPoolExecutor(max_workers=2) as executor:

        results = list(
            executor.map(worker, images)
        )

    return results
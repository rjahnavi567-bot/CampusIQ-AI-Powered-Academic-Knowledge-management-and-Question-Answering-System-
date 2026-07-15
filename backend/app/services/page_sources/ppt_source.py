import os
import shutil
import tempfile

from PIL import Image

import pythoncom

try:
    import win32com.client
except ImportError:
    win32com = None


# ==========================================================
# Loader
# ==========================================================

def load_pages(file_path):

    source = PptSource(file_path)

    images = source.render_pages()

    pages = []

    for i, img in enumerate(images):

        pages.append({

            "page_no": i + 1,

            "image": img

        })

    return pages


# ==========================================================
# PPT Source
# ==========================================================

class PptSource:

    def __init__(self, ppt_path):

        self.ppt_path = os.path.abspath(ppt_path)

    # ------------------------------------------------------

    def render_pages(self):

        if win32com is None:

            raise RuntimeError(

                "pywin32 is not installed.\n"
                "Run: pip install pywin32"

            )

        temp_dir = tempfile.mkdtemp(prefix="ppt_render_")

        pages = []

        powerpoint = None
        presentation = None

        pythoncom.CoInitialize()

        try:

            # ------------------------------------------
            # Start PowerPoint
            # ------------------------------------------

            powerpoint = win32com.client.DispatchEx(
                "PowerPoint.Application"
            )

            powerpoint.Visible = True

            # ------------------------------------------
            # Open Presentation
            # ------------------------------------------

            presentation = powerpoint.Presentations.Open(

                self.ppt_path,

                WithWindow=False

            )

            # ------------------------------------------
            # Export Slides
            # ------------------------------------------

            presentation.Export(

                temp_dir,

                "PNG"

            )

            # ------------------------------------------
            # Read PNGs
            # ------------------------------------------

            files = sorted(

                os.listdir(temp_dir)

            )

            for file in files:

                if not file.lower().endswith(".png"):
                    continue

                img = Image.open(

                    os.path.join(temp_dir, file)

                ).convert("RGB")

                pages.append(img.copy())

                img.close()

        finally:

            # ------------------------------------------
            # Close Presentation
            # ------------------------------------------

            try:

                if presentation is not None:

                    presentation.Close()

            except Exception:
                pass

            # ------------------------------------------
            # Quit PowerPoint
            # ------------------------------------------

            try:

                if powerpoint is not None:

                    powerpoint.Quit()

            except Exception:
                pass

            pythoncom.CoUninitialize()

            # ------------------------------------------
            # Delete Temp Folder
            # ------------------------------------------

            shutil.rmtree(

                temp_dir,

                ignore_errors=True

            )

        return pages
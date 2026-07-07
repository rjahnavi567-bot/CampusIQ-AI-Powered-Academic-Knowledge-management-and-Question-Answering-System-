from .debug_draw import (
    draw_layout,
    draw_regions,
    draw_fusion
)

from .debug_saver import (
    save_render,
    save_layout,
    save_regions,
    save_fusion
)


class PipelineValidator:

    """
    Debug validator for the image extraction pipeline.

    This class DOES NOT modify the pipeline.

    It only:

    • Saves intermediate outputs
    • Prints stage statistics
    • Helps identify where figures disappear
    """

    def __init__(self, output_dir):

        self.output_dir = output_dir

    ##########################################################

    def validate(

        self,

        page_no,

        page_image,

        layout_boxes,

        region_boxes,

        fusion_boxes

    ):

        ##################################################
        # Save original rendered page
        ##################################################

        save_render(

            page_image,

            self.output_dir,

            page_no

        )

        ##################################################
        # Layout Detection
        ##################################################

        layout_img = draw_layout(

            page_image,

            layout_boxes

        )

        save_layout(

            layout_img,

            self.output_dir,

            page_no

        )

        ##################################################
        # Region Detection
        ##################################################

        region_img = draw_regions(

            page_image,

            region_boxes

        )

        save_regions(

            region_img,

            self.output_dir,

            page_no

        )

        ##################################################
        # Fusion Output
        ##################################################

        fusion_img = draw_fusion(

            page_image,

            fusion_boxes

        )

        save_fusion(

            fusion_img,

            self.output_dir,

            page_no

        )

        ##################################################
        # Console Report
        ##################################################

        print()

        print("=" * 60)

        print(f"PAGE {page_no}")

        print("=" * 60)

        print(f"PPStructure Regions : {len(layout_boxes)}")

        print(f"Region Detector     : {len(region_boxes)}")

        print(f"Fusion Output       : {len(fusion_boxes)}")

        print("=" * 60)

        print()
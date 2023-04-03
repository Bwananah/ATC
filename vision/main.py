import constants
import filters
from pipeline import Pipeline
from image_processor import ImageProcessor
from display import Display

# True if we are using the Jetson
using_jetson = False

# filters
depth_frame_filters = [filters.hole_filling()]
color_frame_filters = []
depth_image_filters = []
color_image_filters = []

# instantiate objects
pipeline = Pipeline()  # fetches and processes camera frames
image_processor = ImageProcessor()  # image processing unit
display = Display('ATC: left side warning', width=1280, displaying=not using_jetson)  # displays image and manages window

pipeline.start()
display.start()
try:
    # choose what filters to apply (in-order)
    pipeline.set_depth_frame_filters(depth_frame_filters)
    pipeline.set_color_frame_filters(depth_frame_filters)

    # main loop
    while (not display.isWindowClosed()):
        # wait for new frames
        pipeline.wait_for_frames()

        # apply frame-level filters
        pipeline.apply_filters()

        # get images
        depth_image, color_image = pipeline.get_images()
        image_processor.update_images(depth_image, color_image)

        # apply image-level filters

        # make bounding boxes

        # display informations

        # diplay in window
        display.show(image_processor.depth_image)

finally:
    display.stop()
    pipeline.stop()
import parameters
from pipeline import Pipeline
from image_processor import ImageProcessor
from display import Display

# instantiate objects
pipeline = Pipeline()  # fetches and processes camera frames
image_processor = ImageProcessor()  # image processing unit
display = Display(parameters.window_name, width=parameters.window_width, displaying=not parameters.using_jetson)  # displays image and manages window

pipeline.start()
display.start()
try:
    # choose what filters to apply (in-order)
    pipeline.set_depth_frame_filters(parameters.depth_frame_filters)
    pipeline.set_color_frame_filters(parameters.depth_frame_filters)
    image_processor.set_depth_image_filters(parameters.depth_image_filters)
    image_processor.set_color_image_filters(parameters.color_image_filters)

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
        image_processor.apply_filters()

        # make bounding boxes

        # display informations

        # diplay in window
        display.show(image_processor.depth_image)

finally:
    display.stop()
    pipeline.stop()
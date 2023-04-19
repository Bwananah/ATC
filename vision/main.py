import parameters
from pipeline import Pipeline
from image_processor import ImageProcessor
from display import Display
import numpy as np

# instantiate objects
pipeline = Pipeline()  # fetches and processes camera frames
image_processor = ImageProcessor(parameters.image_cropping)  # image processing unit
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

        # find blobs
        #image_processor.find_blobs(parameters.min_blob_size)

        # make bounding boxes around blobs (and save distances to those blobs)
        #image_processor.make_bounding_boxes(pipeline.get_camera_depths(), pipeline.get_depth_scale())

        # check distance to nearest object, alert if closer than alert distance
        alert = False
        for dist_to_blob in image_processor.distances:
            if dist_to_blob < parameters.alert_dist:
                alert = True

        # diplay in window
        display.show(image_processor.get_images(parameters.display_type), alert)

finally:
    display.stop()
    pipeline.stop()
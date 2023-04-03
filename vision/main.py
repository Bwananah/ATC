import constants
from pipeline import Pipeline
from display import Display

# True if we are using the Jetson
JetsonMode = False

# create objects
pipeline = Pipeline()
display = Display('ATC: left side warning', width=1280, displaying=not JetsonMode)

pipeline.start()
display.start()
try:
    # choose what filters to apply

    # main loop
    while (not display.isWindowClosed()):
        # wait for new frames
        pipeline.wait_for_frames()

        # apply frame-level filters

        # get images
        depth_image, color_image = pipeline.get_images()

        # apply image-level filters

        # make bounding boxes

        # display informations

        # diplay in window
        display.show(color_image)

finally:
    display.stop()
    pipeline.stop()
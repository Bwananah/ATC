import parameters
from pipeline import Pipeline
from image_processor import ImageProcessor
from display import Display
from reminder import Reminder
#import Jetson.GPIO as GPIO
import wave
import subprocess
import time

GREEN_LED = 12
RED_LED = 15
ORANGE_LED = 13
input_pin = 33  

#start_detection = False
#alert = False

  

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(GREEN_LED, GPIO.OUT)
#GPIO.setup(ORANGE_LED, GPIO.OUT)
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(input_pin, GPIO.IN)
#GPIO.add_event_detect(input_pin, GPIO.BOTH, callback=button_callback, bouncetime=200)
#GPIO.output(GREEN_LED, True)	 
#GPIO.output(ORANGE_LED, True)	 
#GPIO.output(GREEN_LED, False)	 
#GPIO.output(ORANGE_LED, False)	 
    

# instantiate objects
pipeline = Pipeline()  # fetches and processes camera frames
image_processor = ImageProcessor(parameters.detection_cropping, parameters.image_cropping)  # image processing unit
display = Display(parameters.window_name, width=parameters.window_width, displaying=not parameters.using_jetson)  # displays image and manages window
reminder = Reminder(parameters.reminder_interval, parameters.reminder_min_delay)  # reminds the challenger in random intervals or when a detection occured
pipeline.start()
display.start()
reminder.start()


try:
    # choose what filters to apply (in-order)
    pipeline.set_depth_frame_filters(parameters.depth_frame_filters)
    pipeline.set_color_frame_filters(parameters.depth_frame_filters)
    image_processor.set_depth_image_filters(parameters.depth_image_filters)
    image_processor.set_color_image_filters(parameters.color_image_filters)
    #GPIO.output(GREEN_LED, True)
    # main loop
   # start_time = time.time()
   # stop_time = 0
    while (True):
        # calculate time it takes to process a frame
    #    start_time = time.time()       
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
        image_processor.find_blobs(parameters.min_blob_size)

        # make bounding boxes around blobs (and save distances to those blobs)
        image_processor.make_bounding_boxes(pipeline.get_camera_depths(), pipeline.get_depth_scale())

        # check distance to nearest object, alert if closer than alert distance
        
        for dist_to_blob in image_processor.distances:
            if dist_to_blob < parameters.alert_dist:
                reminder.remind(True)

     #   stop_time = time.time()
#        print("time: ", stop_time - start_time)

finally:
    display.stop()
    pipeline.stop()
    reminder.stop()
    #GPIO.cleanup()
    #GPIO.output(GREEN_LED, False)	 
    #GPIO.output(ORANGE_LED, False)	 
    

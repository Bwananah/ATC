import pyrealsense2 as rs
import numpy as np
import cv2

# Constants
INFO_POS = (0, 30)
INFO_FONT = cv2.FONT_HERSHEY_SIMPLEX
INFO_SIZE = 1
INFO_COLOR = (255, 255, 255)
INFO_THICKNESS = 2

# Create a context object. This object owns the handles to all connected realsense devices
pipeline = rs.pipeline()
colorizer = rs.colorizer(2)
hole_filling = rs.hole_filling_filter()

pipeline.start()

try:
    while True:
        # Create a pipeline object. This object configures the streaming camera and owns it's handle
        frames = pipeline.wait_for_frames()
        depth = frames.get_depth_frame()
        if not depth: continue

        # Use filter(s)
        #filled_depth = hole_filling.process(depth)
        depth_colormap = np.asanyarray(colorizer.colorize(depth).get_data())
        #
        depth_colormap = cv2.bilateralFilter(depth_colormap, 15, 75, 75)
        #depth_colormap = cv2.GaussianBlur(depth_colormap, (3, 3), 2, cv2.BORDER_DEFAULT)

        
        

        # Show image
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', depth_colormap)
        key = cv2.waitKey(1)

        # Check if window was closed (can use ESC)
        if key == 27 or cv2.getWindowProperty('RealSense',cv2.WND_PROP_VISIBLE) < 1:        
            print('Window was closed')
            cv2.destroyAllWindows()
            break

finally:
    cv2.destroyAllWindows()
    pipeline.stop()
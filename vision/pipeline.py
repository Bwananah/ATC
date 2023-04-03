import cv2
import constants
import pyrealsense2 as rs
import numpy as np

class Pipeline():
    def __init__(self):
        self.pipeline = pipeline = rs.pipeline()  # fetches frames
        self.profile = None  # describes properties of the frames
        self.align = rs.align(rs.stream.color)  # alignes depth and color frames

        self.colorizer = rs.colorizer(constants.COLORIZER_CMAP)  # used to colorize the depth (depth -> RGB)

        self.depth_frame = None  # current depth frame
        self.color_frame = None  # current color frame
    
    # make pipeline start fetching frames
    def start(self):
        self.profile = self.pipeline.start()
    
    # clean up
    def stop(self):
        self.pipeline.stop()
    
    # wait and fetch depth and color frames
    def wait_for_frames(self):
        # reset frames
        self.depth_frame = None
        self.color_frame = None

        while (not self.depth_frame or not self.color_frame):  # Only return when both frames are found
            frames = self.pipeline.wait_for_frames()
            aligned_frames = self.align.process(frames)  # align frames

            self.depth_frame = aligned_frames.get_depth_frame()
            self.color_frame = aligned_frames.get_color_frame()
    
    # get current depth and color as images
    def get_images(self):
        # depth
        colorized_depth_frame = self.colorizer.colorize(self.depth_frame)  # translate depth to color using colorizer
        depth = np.asanyarray(colorized_depth_frame.get_data())

        # color
        color = np.asanyarray(self.color_frame.get_data())
        color = cv2.cvtColor(color, constants.BGR_TO_RGB)  # change image colors from BGR TO RGB

        return depth, color

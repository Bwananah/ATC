import cv2
import constants
import pyrealsense2 as rs
import numpy as np

""" Responsible for processing the camera output streams """
class Pipeline():
    def __init__(self):
        self.pipeline = pipeline = rs.pipeline()  # fetches frames
        self.profile = None  # describes properties of the frames
        self.align = rs.align(rs.stream.color)  # alignes depth and color frames

        self.colorizer = rs.colorizer(constants.COLORIZER_CMAP)  # used to colorize the depth (depth -> RGB)

        self.depth_frame = None  # current depth frame
        self.color_frame = None  # current color frame

        self.depth_frame_filters = []  # filters to apply to the depth frame (in-order)
        self.color_frame_filters = []  # filters to apply to the color frame (in-order)
    
    # Makes pipeline start fetching frames
    def start(self):
        self.profile = self.pipeline.start()
        self.profile.get_device().query_sensors()[0].set_option(rs.option.laser_power, 360) # set laser power (in mW)
    
    # Clean up
    def stop(self):
        self.pipeline.stop()
    
    # Waits and fetches depth and color frames
    def wait_for_frames(self):
        # reset frames
        self.depth_frame = None
        self.color_frame = None

        while (not self.depth_frame or not self.color_frame):  # Only return when both frames are found
            frames = self.pipeline.wait_for_frames()
            aligned_frames = self.align.process(frames)  # align frames

            self.depth_frame = aligned_frames.get_depth_frame()
            self.color_frame = aligned_frames.get_color_frame()
    
    # Gets current depth and color as images
    def get_images(self):
        # depth
        colorized_depth_frame = self.colorizer.colorize(self.depth_frame)  # translate depth to color using colorizer
        depth = np.asanyarray(colorized_depth_frame.get_data())

        # color
        color = np.asanyarray(self.color_frame.get_data())
        color = cv2.cvtColor(color, constants.BGR_TO_RGB)  # change image colors from BGR TO RGB

        return depth, color
    
    # Sets the filters to apply to the depth frame (in-order)
    def set_depth_frame_filters(self, filters):
        self.depth_frame_filters = filters
    
    # Sets the filters to apply to the color frame (in-order)
    def set_color_frame_filters(self, filters):
        self.color_frame_filters = filters
    
    # Applies all filters in-order to both frames
    def apply_filters(self):
        for filter in self.depth_frame_filters:
            self.depth_frame = filter(self.depth_frame)
        
        for filter in self.color_frame_filters:
            self.color_frame = filter(self.color_frame)

    # Gets the depth scale (used for converting camera distances to meters)
    def get_depth_scale(self):
        return self.profile.get_device().first_depth_sensor().get_depth_scale()
    
    # Gets original depth
    def get_camera_depths(self):
        return np.asanyarray(self.depth_frame.get_data())

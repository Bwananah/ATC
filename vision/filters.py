import constants
import pyrealsense2 as rs
import numpy as np


# realsense's hole filling function
def hole_filling():
    hole_filling = rs.hole_filling_filter()

    def filter(frame):
        return hole_filling.process(frame)
    
    return filter

# threshold color channel (channel = 'r', 'g', 'b')
def threshold(thresh, channel):
    index = constants.COLOR_INDEX[channel]  # get index of color channel

    def filter(image):
        # if channel < thresh, 0 else 255
        bin_img = np.zeros(image.shape[0:2])
        bin_img[image[:, :, index] >= thresh] = 255

        return bin_img
    
    return filter
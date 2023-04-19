import constants
import pyrealsense2 as rs
import numpy as np
import cv2


# realsense's hole filling function
def hole_filling():
    hole_filling = rs.hole_filling_filter()

    def filter(frame):
        return hole_filling.process(frame)
    
    return filter

# realsense's decimation function
def decimation(magnitude):
    decimation = rs.decimation_filter()
    decimation.set_option(rs.option.filter_magnitude, magnitude)

    def filter(frame):
        return decimation.process(frame)
    
    return filter

# apply a gaussian blur 
def gaussian_blur(kernel_size, sigma):

    def filter(image):
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma, constants.GAUSSIAN_BLUR_BORDER)
    
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
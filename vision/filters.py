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

# realsense's spatial function
def spatial(magnitude, alpha, delta):
    spatial = rs.spatial_filter()
    spatial.set_option(rs.option.filter_magnitude, magnitude)
    spatial.set_option(rs.option.filter_smooth_alpha, alpha)
    spatial.set_option(rs.option.filter_smooth_delta, delta)

    def filter(frame):
        return spatial.process(frame)
    
    return filter

# realsense's temporal function
def temporal(alpha, delta):
    temporal = rs.temporal_filter()
    temporal.set_option(rs.option.filter_smooth_alpha, alpha)
    temporal.set_option(rs.option.filter_smooth_delta, delta)

    def filter(frame):
        return temporal.process(frame)
    
    return filter

# gaussian blur 
def gaussian_blur(kernel_size, sigma):

    def filter(image):
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma, constants.GAUSSIAN_BLUR_BORDER)
    
    return filter

# threshold color channel (channel = 'r', 'g', 'b')
def threshold(thresh, channel):
    index = constants.COLOR_INDEX[channel]  # get index of color channel

    def filter(image):
        # stretch values so that min = 0 and max = 255
        stretched = ((image - image.min()) / (image.max() - image.min()) * 255).astype(int)

        # if channel < thresh, 0 else 255
        bin_img = np.zeros(stretched.shape[0:2])
        bin_img[stretched[:, :, index] >= thresh] = 255

        return bin_img
    
    return filter

# bilateral filter
def bilateral(d, sigma_color, sigma_dist):

    def filter(image):
        return cv2.bilateralFilter(image, d, sigma_color, sigma_dist)
    
    return filter
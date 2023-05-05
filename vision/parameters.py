import filters

# True if we are using the Jetson
using_jetson = False

# window parameters
window_width = 400
window_name = 'ATC: left side warning'
display_type = 'both'  # 'color', 'depth' or 'both'

# image cropping parameters (how much to crop from each side, in pixels)
detection_cropping = (100, 300, 100, 200)  # (left, right, top, bottom)
image_cropping = (0, 0, 0, 200)

# alert
alert_dist = 3 # alert distance (in meters)
alert_msg = 'ALERTE'

# timer
reminder_interval = [120, 180]  # random time interval to remind the Challenger (in seconds)
reminder_min_delay = 30  # time until new reminder if continuously in alert state (in seconds)

# filter parameters
decimation_magnitude = 2
spatial_magnitude = 2
spatial_alpha = 0.5
spatial_delta = 20
temporal_alpha = 0.4
temporal_delta = 20
gaussian_kernel_size = 3
gaussian_sigma = 2
bilateral_d = 15
bilateral_sigma_color = 75
bilateral_sigma_dist = 75
depth_threshold = 150
min_blob_size = 8000

# filters
depth_frame_filters = []  # decimation, spatial, temporal, hole_filling
color_frame_filters = []
depth_image_filters = [filters.bilateral(bilateral_d, bilateral_sigma_color, bilateral_sigma_dist), filters.gaussian_blur(gaussian_kernel_size, gaussian_sigma), filters.threshold(depth_threshold, 'r')]  # gaussian_blur, threshold
color_image_filters = []

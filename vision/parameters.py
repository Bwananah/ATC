import filters

# True if we are using the Jetson
using_jetson = False

# window parameters
window_width = 600
window_name = 'ATC: left side warning'
display_type = 'both'  # 'color', 'depth' or 'both'

# image cropping parameters (how much to crop from each side, in pixels)
image_cropping = (200, 0, 0, 100)  # (left, right, top, bottom)

# alert
alert_dist = 2.5 # alert distance (in meters)
alert_msg = 'ALERTE'

# timer
reminder_interval = [15, 45]  # random time interval to remind the Challenger (in seconds)
reminder_min_delay = 5  # time until new reminder if continuously in alert state (in seconds)

# filter parameters
decimation_magnitude = 2
spatial_magnitude = 2
spatial_alpha = 0.5
spatial_delta = 20
temporal_alpha = 0.4
temporal_delta = 20
gaussian_kernel_size = 7
gaussian_sigma = 2
depth_threshold = 230
min_blob_size = 10000

# filters
depth_frame_filters = [filters.hole_filling()]  # decimation, spatial, temporal, hole_filling
color_frame_filters = []
depth_image_filters = [filters.gaussian_blur(gaussian_kernel_size, gaussian_sigma), filters.threshold(depth_threshold, 'r')]  # gaussian_blur, threshold
color_image_filters = []
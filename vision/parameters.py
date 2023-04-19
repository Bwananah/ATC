import filters

# True if we are using the Jetson
using_jetson = False

# window parameters
window_width = 1280
window_name = 'ATC: left side warning'
display_type = 'depth'  # 'color', 'depth' or 'both'

# image cropping parameters (how much to crop from each side, in pixels)
image_cropping = (0, 0, 0, 0)  # (left, right, top, bottom)

# alert
alert_dist = 0.8 # alert distance (in meters)
alert_msg = 'ALERTE'

# filter parameters
decimation_magnitude = 2
spatial_magnitude = 2
spatial_alpha = 0.5
spatial_delta = 20
gaussian_kernel_size = 5
gaussian_sigma = 1
depth_threshold = 230
min_blob_size = 10000

# filters
depth_frame_filters = [filters.spatial(spatial_magnitude, spatial_alpha, spatial_delta)]  # decimation, spatial, hole_filling
color_frame_filters = []
depth_image_filters = []#[filters.gaussian_blur(gaussian_kernel_size, gaussian_sigma)]#[filters.threshold(depth_threshold, 'r')]  # gaussian_blur, threshold
color_image_filters = []
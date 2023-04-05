import filters

# True if we are using the Jetson
using_jetson = False

# window parameters
window_width = 600
window_name = 'ATC: left side warning'
display_type = 'both'  # 'color', 'depth' or 'both'

# alert
alert_dist = 0.8 # alert distance (in meters)
alert_msg = 'ALERTE'

# filter parameters
depth_threshold = 230
min_blob_size = 10000

# filters
depth_frame_filters = [filters.hole_filling()]
color_frame_filters = []
depth_image_filters = [filters.threshold(depth_threshold, 'r')]
color_image_filters = []
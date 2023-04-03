import filters

# True if we are using the Jetson
using_jetson = False

# window parameters
window_width = 1280
window_name = 'ATC: left side warning'

# filter parameters
threshold = 230
min_blob_size = 10000

# filters
depth_frame_filters = [filters.hole_filling()]
color_frame_filters = []
depth_image_filters = [filters.threshold(threshold, 'r')]
color_image_filters = []
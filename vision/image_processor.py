class ImageProcessor:
    def __init__(self):
        self.depth_image = None  # current depth image
        self.color_image = None  # current color image

        self.depth_image_filters = []  # filters to apply to the depth image (in-order)
        self.color_image_filters = []  # filters to apply to the color image (in-order)

    # update current image
    def update_images(self, depth, color):
        self.depth_image = depth
        self.color_image = color
    
    # Set the filters to apply to the depth image (in-order)
    def set_depth_image_filters(self, filters):
        self.depth_image_filters = filters
    
    # Set the filters to apply to the color image (in-order)
    def set_color_image_filters(self, filters):
        self.color_image_filters = filters
    
    # apply all filters in-order to both images
    def apply_filters(self):
        for filter in self.depth_image_filters:
            self.depth_image = filter(self.depth_image)
        
        for filter in self.color_image_filters:
            self.color_image = filter(self.color_image)
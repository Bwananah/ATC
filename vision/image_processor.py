import numpy as np
import cv2
import constants
from skimage import measure


class ImageProcessor:
    def __init__(self):
        self.depth_image = None  # current depth image
        self.color_image = None  # current color image

        self.depth_image_filters = []  # filters to apply to the depth image (in-order)
        self.color_image_filters = []  # filters to apply to the color image (in-order)

        self.labels = []  # blob labels
        self.distances = []  # distance to each blob

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
    
    def find_blobs(self, min_blob_size):
        self.labels = measure.label(self.depth_image).astype(np.uint8) # label each pixel as same blob if connected
        labels_copy = np.copy(self.labels)

        nb_blobs = np.amax(self.labels)
        for i in range(nb_blobs+1):
            num_pixels = sum(sum(self.labels==i))  # count number of pixels in blob i

            # remove small blobs
            if num_pixels < min_blob_size:
                labels_copy[self.labels==i] = 0
        
        self.labels = labels_copy  # labels left are only those of big blobs

        # update depth image to only show those blobs
        white_where_blob = np.where(self.labels > 0, 255, 0).astype(np.uint8)  # convert all non-zero labeled pixels to 255
        self.depth_image = cv2.merge((white_where_blob, white_where_blob, white_where_blob))
    
    # create bbox around blobs and get their distances from original camera depth
    def make_bounding_boxes(self, camera_depth, depth_scale):
        # reset distances
        self.distances = []

        # for each blob
        for i in np.unique(self.labels)[1:]:
            # get corners of bbox
            blob_coords = np.where(self.labels == i) # image coordinates of all of that blob's pixels
            xmin = np.min(blob_coords[1])
            xmax = np.max(blob_coords[1])
            ymin = np.min(blob_coords[0])
            ymax = np.max(blob_coords[0])

            # get distance to object
            dist = depth_scale * camera_depth[blob_coords[0], blob_coords[1]].astype(float)  # convert distances to meters
            dist = np.mean(dist)  # get mean distance to blob
            self.distances.append(dist)  # all distances stored (in meters)

            # add bbox to both images
            cv2.rectangle(self.color_image, (xmin, ymin), (xmax, ymax), constants.BBOX_COLOR, constants.BBOX_THICKNESS)
            cv2.rectangle(self.depth_image, (xmin, ymin), (xmax, ymax), constants.BBOX_COLOR, constants.BBOX_THICKNESS)

            # add text over bbox to both images
            cv2.putText(self.color_image,
                         f'{dist:.2f} m',
                        (xmin, ymin - constants.BBOX_TEXT_OFFSET),
                        constants.BBOX_FONT,
                        constants.BBOX_TEXT_THICKNESS,
                        constants.BBOX_COLOR)
            cv2.putText(self.depth_image,
                        f'{dist:.2f} m',
                        (xmin, ymin - constants.BBOX_TEXT_OFFSET),
                        constants.BBOX_FONT,
                        constants.BBOX_TEXT_THICKNESS,
                        constants.BBOX_COLOR)
import pyrealsense2 as rs
import numpy as np
import cv2
from skimage import measure, color

def remove_noise(cc_ids,threshold):

    label_img_new = np.copy(cc_ids)
    num_comp = np.amax(cc_ids)
    
    for i in range(num_comp+1):
        num_pixels = sum(sum(cc_ids==i))
        if num_pixels < threshold:
            label_img_new[cc_ids==i] = 0
    
    return label_img_new

# Constants
INFO_POS = (0, 30)
INFO_FONT = cv2.FONT_HERSHEY_SIMPLEX
INFO_SIZE = 1
INFO_COLOR = (255, 255, 255)
INFO_THICKNESS = 2

THRESHOLD = 220
BLOB_SIZE_THRESHOLD = 1000

# Create a context object. This object owns the handles to all connected realsense devices
pipeline = rs.pipeline()
colorizer = rs.colorizer(2) # white-to-black
hole_filling = rs.hole_filling_filter()

pipeline.start()

try:
    while True:
        # Create a pipeline object. This object configures the streaming camera and owns it's handle
        frames = pipeline.wait_for_frames()
        depth = frames.get_depth_frame()
        if not depth: continue

        # Use filter(s)
        filled_depth = hole_filling.process(depth)
        depth_colormap = np.asanyarray(colorizer.colorize(filled_depth).get_data())

        # because white-to-black -> only care about one channel
        bin_img = np.zeros(depth_colormap.shape[0:2])
        bin_img.fill(255)
        bin_img[depth_colormap[:, :, 0] < THRESHOLD] = 0

        labels = measure.label(bin_img).astype(np.uint8) # count blobs
        denoised = remove_noise(labels, BLOB_SIZE_THRESHOLD) # Only get blobs bigger than threshold
            
        # convert back to color
        test = np.where(denoised > 0, 255, 0).astype(np.uint8)
        test = cv2.merge((test,test,test)) # one channel to 3

        # Make bounding box
        for i in np.unique(denoised)[1:]:
            indices = np.where(denoised == i) # indices where that blob was found
            xmin = np.min(indices[1])
            xmax = np.max(indices[1])
            ymin = np.min(indices[0])
            ymax = np.max(indices[0])

            cv2.rectangle(test, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        
        # display information on screen
        #info = np.max(depth_colormap)
        #depth_colormap = cv2.putText(depth_colormap, f'{info}', INFO_POS, INFO_FONT, INFO_SIZE, INFO_COLOR, INFO_THICKNESS, cv2.LINE_AA)

        # Show image
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', test)
        key = cv2.waitKey(1)

        # Check if window was closed (can use ESC)
        if key == 27 or cv2.getWindowProperty('RealSense',cv2.WND_PROP_VISIBLE) < 1:        
            print('Window was closed')
            cv2.destroyAllWindows()
            break

finally:
    cv2.destroyAllWindows()
    pipeline.stop()
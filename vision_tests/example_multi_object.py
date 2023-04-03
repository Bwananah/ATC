import cv2                                # state of the art computer vision algorithms library
import numpy as np                        # fundamental package for scientific computing
import pyrealsense2 as rs                 # Intel RealSense cross-platform open-source API
print("Environment Ready")


# Resizes images
def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

# Setup:
pipeline = rs.pipeline()
colorizer = rs.colorizer()

profile = pipeline.start()
try:
    while True:
        # Store next frameset for later processing:
        frameset = pipeline.wait_for_frames()
        color_frame = frameset.get_color_frame()
        depth_frame = frameset.get_depth_frame()
        if not depth_frame or not color_frame: continue

        # Get images
        color = np.asanyarray(color_frame.get_data())
        color = cv2.cvtColor(color, cv2.COLOR_BGR2RGB)
        colorized_depth = np.asanyarray(colorizer.colorize(depth_frame).get_data())

        # Align both streams to color stream
        align = rs.align(rs.stream.color)
        frameset = align.process(frameset)

        # Update color and depth frames:
        aligned_depth_frame = frameset.get_depth_frame()
        colorized_depth = np.asanyarray(colorizer.colorize(aligned_depth_frame).get_data())

        # Standard OpenCV boilerplate for running the net:
        height, width = color.shape[:2]
        expected = 300
        aspect = width / height
        resized_image = cv2.resize(color, (round(expected * aspect), expected))
        crop_start = round(expected * (aspect - 1) / 2)
        crop_img = resized_image[0:expected, crop_start:crop_start+expected]

        net = cv2.dnn.readNetFromCaffe("./MobileNetSSD_deploy.prototxt", "./MobileNetSSD_deploy.caffemodel")
        inScaleFactor = 0.007843
        meanVal       = 127.53
        classNames = ("background", "aeroplane", "bicycle", "bird", "boat",
                    "bottle", "bus", "car", "cat", "chair",
                    "cow", "diningtable", "dog", "horse",
                    "motorbike", "person", "pottedplant",
                    "sheep", "sofa", "train", "tvmonitor")

        blob = cv2.dnn.blobFromImage(crop_img, inScaleFactor, (expected, expected), meanVal, False)
        net.setInput(blob, "data")
        detections = net.forward("detection_out")
        
        for i in np.arange(0, detections.shape[2]):

            label = detections[0,0,i,1]
            conf  = detections[0,0,i,2]
            xmin  = detections[0,0,i,3]
            ymin  = detections[0,0,i,4]
            xmax  = detections[0,0,i,5]
            ymax  = detections[0,0,i,6]
            
            className = classNames[int(label)]

            if conf > 0.8:
                cv2.rectangle(crop_img, (int(xmin * expected), int(ymin * expected)), 
                            (int(xmax * expected), int(ymax * expected)), (255, 255, 255), 2)
                
                scale = height / expected
                xmin_depth = int((xmin * expected + crop_start) * scale)
                ymin_depth = int((ymin * expected) * scale)
                xmax_depth = int((xmax * expected + crop_start) * scale)
                ymax_depth = int((ymax * expected) * scale)
                xmin_depth,ymin_depth,xmax_depth,ymax_depth
                #cv2.rectangle(colorized_depth, (xmin_depth, ymin_depth), (xmax_depth, ymax_depth), (255, 255, 255), 2)
                
                depth = np.asanyarray(aligned_depth_frame.get_data())
                # Crop depth data:
                depth = depth[xmin_depth:xmax_depth,ymin_depth:ymax_depth].astype(float)

                # Get data scale from the device and convert to meters
                depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()
                depth = depth * depth_scale
                dist,_,_,_ = cv2.mean(depth)

                # print distance and class
                cv2.putText(crop_img, "{0}: {1:.3} m.".format(className, dist), 
                            (int(xmin * expected), int(ymin * expected) - 5),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255))

        # Show image
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        #images = np.hstack((crop_img, colorized_depth))
        imS = ResizeWithAspectRatio(crop_img, width=700) # resize window
        cv2.imshow('RealSense', imS)
        key = cv2.waitKey(1)

        # Check if window was closed (can use ESC)
        if key == 27 or cv2.getWindowProperty('RealSense',cv2.WND_PROP_VISIBLE) < 1:        
            print('Window was closed')
            cv2.destroyAllWindows()
            break

finally:
    cv2.destroyAllWindows()
    pipeline.stop()
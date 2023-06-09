import pyrealsense2 as rs
import numpy as np
import cv2
import Jetson.GPIO as GPIO
from skimage import measure, color
import wave
import alsaaudio

def remove_noise(cc_ids,threshold):

    label_img_new = np.copy(cc_ids)
    num_comp = np.amax(cc_ids)
    
    for i in range(num_comp+1):
        num_pixels = sum(sum(cc_ids==i))
        if num_pixels < threshold:
            label_img_new[cc_ids==i] = 0
    
    return label_img_new

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

# Constants
INFO_POS = (0, 30)
INFO_FONT = cv2.FONT_HERSHEY_SIMPLEX
INFO_SIZE = 1
INFO_COLOR = (255, 255, 255)
INFO_THICKNESS = 2

THRESHOLD = 230
BLOB_SIZE_THRESHOLD = 10000

GREEN_LED = 12
RED_LED = 15
ORANGE_LED = 13

alert_cnt = 0

# Create a context object. This object owns the handles to all connected realsense devices
pipeline = rs.pipeline()
colorizer = rs.colorizer(2) # white-to-black
hole_filling = rs.hole_filling_filter()

# Align depth and color streams
align_to = rs.stream.color
align = rs.align(align_to)

profile = pipeline.start()

try:
    audio_file = wave.open('voice.wav', 'rb') 
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GREEN_LED, GPIO.OUT)
    GPIO.setup(RED_LED, GPIO.OUT)
    GPIO.setup(ORANGE_LED, GPIO.OUT)

    GPIO.output(GREEN_LED, True)
    
    alerte = False
    cnt = 0

    channels = audio_file.getnchannels()
    sample_rate = audio_file.getframerate()
    format = audio_file.getsampwidth()

    # Open the audio card for playback
    output_device = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK)
    output_device.setchannels(audio_file.getnchannels())
    output_device.setrate(audio_file.getframerate())
    output_device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    output_device.setperiodsize(1024)

    print("Starting....")

    while True:
        # Create a pipeline object. This object configures the streaming camera and owns it's handle
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()
        if not depth_frame or not color_frame:
            continue

        # color img
        color = np.asanyarray(color_frame.get_data())
        color = cv2.cvtColor(color, cv2.COLOR_BGR2RGB)

        # Use filter(s)
        filled_depth = hole_filling.process(depth_frame)
        depth_colormap = np.asanyarray(colorizer.colorize(filled_depth).get_data())

        # because white-to-black -> only care about one channel
        bin_img = np.zeros(depth_colormap.shape[0:2])
        bin_img.fill(255)
        bin_img[depth_colormap[:, :, 0] < THRESHOLD] = 0

        labels = measure.label(bin_img).astype(np.uint8) # count blobs
        denoised = remove_noise(labels, BLOB_SIZE_THRESHOLD) # Only get blobs bigger than threshold
            
        # convert back to color
        #test = np.where(denoised > 0, 255, 0).astype(np.uint8)
        #test = cv2.merge((test,test,test)) # one channel to 3

        # Make bounding box and print distance to blob
        depth = np.asanyarray(depth_frame.get_data())

        alerte = False
        GPIO.output(ORANGE_LED, True)
        for i in np.unique(denoised)[1:]:
            # bbox
            indices = np.where(denoised == i) # indices where that blob was found
            xmin = np.min(indices[1])
            xmax = np.max(indices[1])
            ymin = np.min(indices[0])
            ymax = np.max(indices[0])
            cv2.rectangle(color, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2) #bbox
            
            # dist
            depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()
            dist = depth_scale * depth[indices[0],indices[1]].astype(float)
            dist = np.mean(dist)
            if dist < 0.4: # Alert if closer than 40 cm
                alerte = True
                break
            cv2.putText(color, "{0:.3} m.".format(dist), 
                            (xmin, ymin - 5),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,255,0)) # text
        
        GPIO.output(ORANGE_LED, False)        
        # display information on screen
        info = ""

        GPIO.output(RED_LED, alerte)
        
        if alerte == True: 
            info = "ALERTE"
            alert_cnt += 1           
            audio_file.rewind()
            while True:
                data = audio_file.readframes(1024)
                if not data:
                    break
                output_device.write(data)

            print(info, alert_cnt)
        
        cnt += 1
        print("No alerte", cnt)
        

finally:
#    cv2.destroyAllWindows()
    pipeline.stop()
    GPIO.output(GREEN_LED, False)
    GPIO.cleanup()
    output_device.close()
    audio_file.close()
    print("Finished")

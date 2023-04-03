import cv2
import constants

class Display():
    def __init__(self, name, width):
        self.name = name
        self.width = width

    # create window
    def start(self):
        cv2.namedWindow(self.name, constants.WINDOW_SIZE_FLAG)

    # closes window
    def stop(self):
        cv2.destroyAllWindows()
    
    # show image on display
    def show(self, image):
        img = self.resizeWithAspectRatio(image)
        cv2.imshow(self.name, img)

    # check if user wants to close the window (ESC key or manually closing window)
    def isWindowClosed(self, verbose=True):
        key = cv2.waitKey(1)  # Get user key press

        # check if user closed the window
        if key == constants.ESC_KEY or cv2.getWindowProperty(self.name, constants.WINDOW_STATE_FLAG) < 1: 
            if verbose:       
                print('Window was closed')
            return True
        
        return False
    
    # resizes images to window width while keeping the original aspect ratio
    def resizeWithAspectRatio(self, image):
        (h, w) = image.shape[:2]
        r = self.width / float(w)
        dim = (self.width, int(h * r))

        return cv2.resize(image, dim, interpolation=constants.WINDOW_RESIZE_INTERPOLATION)
    
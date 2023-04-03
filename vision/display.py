import cv2
import constants

class Display():
    def __init__(self, name):
        self.name = name

    # create window
    def start(self):
        cv2.namedWindow(self.name, constants.WINDOW_SIZE_FLAG)

    # closes window
    def stop(self):
        cv2.destroyAllWindows()
    
    # show image on display
    def show(self, image):
        cv2.imshow(self.name, image)

    # check if user wants to close the window (ESC key or manually closing window)
    def isWindowClosed(self, verbose=True):
        key = cv2.waitKey(1)  # Get user key press

        # check if user closed the window
        if key == constants.ESC_KEY or cv2.getWindowProperty(self.name, constants.WINDOW_STATE_FLAG) < 1: 
            if verbose:       
                print('Window was closed')
            return True
        
        return False
    
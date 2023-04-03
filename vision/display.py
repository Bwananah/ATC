import cv2
import constants
import keyboard

class Display():
    def __init__(self, name, width, displaying):
        self.name = name  # window name
        self.width = width  # window width
        self.displaying = displaying  # True if we want to display to a screen, False if we don't

    # create window
    def start(self):
        if self.displaying:
            cv2.namedWindow(self.name, constants.WINDOW_SIZE_FLAG)

    # closes window
    def stop(self):
        if self.displaying:
            cv2.destroyAllWindows()
    
    # show image on display
    def show(self, image):
        if self.displaying:
            img = self.resizeWithAspectRatio(image)
            cv2.imshow(self.name, img)

    # check if user wants to close the window (ESC key or manually closing window)
    def isWindowClosed(self, verbose=True):
        # if displaying, check if window was closed
        if self.displaying:
            key = cv2.waitKey(1)  # Get user key press

            # check if user closed the window
            if key == constants.WINDOW_ESC_KEY or cv2.getWindowProperty(self.name, constants.WINDOW_STATE_FLAG) < 1: 
                if verbose:       
                    print('Window was closed')
                return True
        else:  # if not displaying, check if program needs to stop
            if keyboard.is_pressed(constants.CONSOLE_ESC_KEY):
                if verbose:       
                    print('Program was stopped')
                return True
        
        return False
    
    # resizes images to window width while keeping the original aspect ratio
    def resizeWithAspectRatio(self, image):
        (h, w) = image.shape[:2]
        r = self.width / float(w)
        dim = (self.width, int(h * r))

        return cv2.resize(image, dim, interpolation=constants.WINDOW_RESIZE_INTERPOLATION)
    
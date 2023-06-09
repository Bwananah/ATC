import cv2
import constants
import parameters

""" Displays information to the screen (if not on Jetson ) """
class Display():
    def __init__(self, name, width, displaying):
        self.name = name  # window name
        self.width = width  # window width
        self.displaying = displaying  # True if we want to display to a screen, False if we don't

    # Creates window
    def start(self):
        if self.displaying:
            cv2.namedWindow(self.name, constants.WINDOW_SIZE_FLAG)

    # Closes window
    def stop(self):
        if self.displaying:
            cv2.destroyAllWindows()
    
    # Shows image on display
    def show(self, image, alert):
        if self.displaying:
            # resize image
            img = self.resizeWithAspectRatio(image)

            # show alert message if needed
            if alert:
                # background
                text_size = cv2.getTextSize(f'{parameters.alert_msg}',
                                                          constants.INFO_FONT,
                                                          constants.INFO_SIZE,
                                                          constants.INFO_THICKNESS)
                img = cv2.rectangle(img,
                                    (constants.INFO_POS[0], constants.INFO_POS[1] + 5),
                                    (constants.INFO_POS[0] + text_size[0][0], constants.INFO_POS[1] - text_size[0][1] - 5),
                                    constants.INFO_BACKGROUND,
                                    -1)
                
                # text
                img = cv2.putText(img,
                                  f'{parameters.alert_msg}',
                                  constants.INFO_POS,
                                  constants.INFO_FONT,
                                  constants.INFO_SIZE,
                                  constants.INFO_COLOR,
                                  constants.INFO_THICKNESS,
                                  constants.LINE_TYPE)

            cv2.imshow(self.name, img)

    # Checks if user wants to close the window (ESC key or manually closing window)
    def isWindowClosed(self):
        if self.displaying:
            # if displaying, check if window was closed
            key = cv2.waitKey(1)  # Get user key press

            # check if user closed the window
            if key == constants.WINDOW_ESC_KEY or cv2.getWindowProperty(self.name, constants.WINDOW_STATE_FLAG) < 1:       
                print('Window was closed')
                return True
            
        return False
    
    # Resizes images to window width while keeping the original aspect ratio
    def resizeWithAspectRatio(self, image):
        (h, w) = image.shape[:2]
        r = self.width / float(w)
        dim = (self.width, int(h * r))

        return cv2.resize(image, dim, interpolation=constants.WINDOW_RESIZE_INTERPOLATION)
    
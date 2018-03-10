# import the necessary packages
import skimage 

from skimage.transform import resize

class SimplePreprocessor:
    def __init__(self, width, height):
        # store the target image width, height
        self.width  = width
        self.height = height

    def preprocess(self, image):
        # resize the image to a fixed size, ignoring the aspect
        # ratio
        return resize(image, (self.width, self.height))

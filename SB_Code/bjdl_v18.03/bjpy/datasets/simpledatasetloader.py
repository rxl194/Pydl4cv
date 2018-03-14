# import the necessary packages
import numpy as np
import cv2
import os

class SimpleDatasetLoader:
    def __init__(self, preprocessors=None):
        # store the image preprocessor
        self.preprocessors = preprocessors

        # if the preprocessors are None, initialize them as an
        # empty list
        if self.preprocessors is None:
            self.preprocessors = []

    def load(self, image_root, images, in_labels, verbose=-1):
        # initialize the list of features and labels
        i = 0
        data = []
        labels = []

        # loop over the input images
        for (imagefile, label) in zip(images, in_labels):
            # load the image and extract the class label assuming
            # that our path has the following format:
            # image_root/{label}/imagefile
            i += 1
            imagePath = os.path.join(image_root, label, imagefile)
            image = cv2.imread(imagePath)

            # check to see if our preprocessors are not None
            if self.preprocessors is not None:
                # loop over the preprocessors and apply each to
                # the image
                for p in self.preprocessors:
                    image = p.preprocess(image)

            # treat our processed image as a "feature vector"
            # by updating the data list followed by the labels
            data.append(image)
            labels.append(label)

            # show an update every `verbose` images
            if verbose > 0 and i % verbose == 0:
                print("[INFO] processed {}/{}".format(i,
                    len(images)))

        # return a tuple of the data and labels
        return (np.array(data), np.array(labels))

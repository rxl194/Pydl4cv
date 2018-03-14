# import the necessary packages
import os

from tensorflow.python.lib.io import file_io

class GcsImageLabelReader:

    def __init__(self, gcs_csv):
        path_sep = gcs_csv.rfind('/')
        self.gcs_root = gcs_csv[:path_sep-1]
        self.csv_dataset = gcs_csv


    def read_img_label(self):
        images = []
        labels = []
        with file_io.FileIO(self.csv_dataset, mode='r') as fp:
            for line in fp:
                bufs = line.split(",")
                image_file = bufs[0].strip()
                label = bufs[1].strip()
                images.append(image_file)
                labels.append(label)
        return self.gcs_root, images, labels


    
      

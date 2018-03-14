# import the necessary packages
import os

from tensorflow.python.lib.io import file_io

class GcsImageLabelReader:

    def __init__(self, gcs_csv):
        path_sep = gcs_csv.rfind('/')
        self.gcs_root = gcs_csv[:path_sep-1]
        self.csf_file = gcs_csv[path_sep+1:]


    def read_img_label(self):
        return self.gcs_root, self.csf_file


    
      

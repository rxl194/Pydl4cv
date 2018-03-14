# import the necessary packages
import os
import pickle
import json

from tensorflow.python.lib.io import file_io

class GcsImageLabelReader:

    def __init__(self, dataset_json):
        path_sep = dataset_json.rfind('/')
        self.gcs_root = dataset_json[:path_sep]
        self.dataset_json = dataset_json


    def read_img_label(self):
        data  = None
        laels = None
        with file_io.FileIO(self.dataset_json, mode='r') as fp:
            datafiles = json.load(fp)
        
        data_f = os.path.join(self.gcs_root,datafiles["data"])
        print("[INFO] data_f: ", data_f)
        with file_io.FileIO(data_f, mode='rb') as fp:
            data = pickle.load(fp)

        label_f = os.path.join(self.gcs_root,datafiles["label"])
        print("[INFO] label_f: ", label_f)
        with file_io.FileIO(label_f, mode='rb') as fp:
            labels = pickle.load(fp)

        return self.gcs_root, data, labels


    
      

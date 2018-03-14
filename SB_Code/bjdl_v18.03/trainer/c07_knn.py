# USAGE
# python trainer/c07_knn.py --dataset ../datasets/animals

# import the necessary packages
import os
import argparse
import pickle
import json

from bjpy.bjutl  import bjutl_paths
from bjpy.gcsutl import gcsutil_paths

from bjpy.preprocessing import SimplePreprocessor
from bjpy.datasets import SimpleDatasetLoader

# construct the argument parse and parse the arguments
def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dataset", required=True,
	    help="path to input dataset")
    ap.add_argument("-k", "--neighbors", type=int, default=1,
	    help="# of nearest neighbors for classification")
    ap.add_argument("--local", action='store_true',
            help="local run")
    ap.add_argument('--job-dir', default="/tmp",
      help='Cloud storage bucket to export the model and store temp files') 
    args = vars(ap.parse_args())
    return args

def load_img_data(dataset):

    imagePaths = list(bjutl_paths.list_images(args["dataset"]))

    return imagePaths

def extract_img_label(datasets, imagePaths):
    of = None
    if None and datasets and len(datasets)>0:
        file_path_sep = datasets.split(os.path.sep)
        filename = "dataset_" + file_path_sep[-1] + ".csv"
        of = open(filename, "w")
        
    images = []
    labels = []
    for (i, imagePath) in enumerate(imagePaths):
        # load the image and extract the class label assuming
        # that our path has the following format:
        # /path/to/dataset/{class}/{image}.jpg
        file_path_sep = imagePath.split(os.path.sep)
        images.append( file_path_sep[-1] )
        labels.append( file_path_sep[-2] )
        if of:
            of.write( file_path_sep[-1] + ", " + file_path_sep[-2] + "\n" )

    if of:
        of.close()
    return images, labels

def read_img_label(dataset):
    gcsPaths = gcsutil_paths.GcsImageLabelReader(dataset)
    return gcsPaths.read_img_label()

def read_img_files(imageRoot, images, labels):
    # initialize the image preprocessor, load the dataset from disk,
    # and reshape the data matrix
    sp = SimplePreprocessor(32, 32)
    sdl = SimpleDatasetLoader(preprocessors=[sp])
    data, labels = sdl.load(imageRoot, images, labels, verbose=500)
    data = data.reshape((data.shape[0], 3072))
    return (data, labels)

def pickle_dump(datasets, imageRoot, data, labels):
    if datasets and len(datasets)>0:
        file_path_sep = datasets.split(os.path.sep)

        data_files = {}
        filename = "data_" + file_path_sep[-1] + ".pkl"
        with open(filename, "wb") as f:
            pickle.dump(data, f)
        data_files["data"] = filename

        filename = "label_" + file_path_sep[-1] + ".pkl"
        with open(filename, "wb") as f:
            pickle.dump(labels, f)
        data_files["label"] = filename

        with open('datasets.json', 'w') as f:
            json.dump(data_files, f)

if __name__ == "__main__":

    args = get_args()

    arg_dataset = args["dataset"]
    print("[INFO] loading dataset images from: ", arg_dataset)

    if ( args["local"] ):
        imagePaths = load_img_data(arg_dataset)
        images, labels = extract_img_label(arg_dataset, imagePaths)
        imageRoot = arg_dataset

        data, labels = read_img_files(imageRoot, images, labels)

        pickle_dump(arg_dataset, imageRoot, data, labels)

    else:
        imageRoot, data, labels = read_img_label(arg_dataset)


    print("[INFO] total data loaded: ", len(data))
    print("[INFO] total label loaded: ", len(labels))



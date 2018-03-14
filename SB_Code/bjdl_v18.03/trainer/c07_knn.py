# USAGE
# python trainer/c07_knn.py --dataset ../datasets/animals

# import the necessary packages
import os
import argparse

from bjutl  import bjutl_paths
from gcsutl import gcsutil_paths

# construct the argument parse and parse the arguments
def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dataset", required=True,
	    help="path to input dataset")
    ap.add_argument("-k", "--neighbors", type=int, default=1,
	    help="# of nearest neighbors for classification")
    ap.add_argument("--local", action='store_true',
            help="local run")
    args = vars(ap.parse_args())
    return args

def load_img_data(dataset):
    print("[INFO] loading dataset images from: ", dataset)

    imagePaths = list(bjutl_paths.list_images(args["dataset"]))
    print ("[INFO] total image loaded: ", len(imagePaths))

    return imagePaths

def extract_img_label(datasets, imagePaths):
    of = None
    if datasets and len(datasets)>0:
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
    images, labels = gcsPaths.read_img_label()
    print images, labels
    return images, labels


if __name__ == "__main__":

    args = get_args()

    arg_dataset = args["dataset"]
    if ( args["local"] ):
        imagePaths = load_img_data(arg_dataset)
        images, labels = extract_img_label(arg_dataset, imagePaths)
    else:
        images, labels = read_img_label(arg_dataset)



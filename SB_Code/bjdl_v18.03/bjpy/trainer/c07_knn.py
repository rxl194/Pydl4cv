# USAGE
# python trainer/c07_knn.py --dataset ../datasets/animals

# import the necessary packages
import os
import argparse
import pickle
import json

from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from bjutl  import bjutl_paths
from gcsutl import gcsutil_paths

from preprocessing import SimplePreprocessor
from datasets import SimpleDatasetLoader

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
    ap.add_argument("-j", "--jobs", type=int, default=-1,
        help="# of jobs for k-NN distance (-1 uses all available cores)")

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

def kNN_train(trainX, trainY):
    # train and evaluate a k-NN classifier on the raw pixel intensities
    print("[INFO] evaluating k-NN classifier...")
    model = KNeighborsClassifier(n_neighbors=args["neighbors"],
        n_jobs=args["jobs"])
    model.fit(trainX, trainY)
    return model
                                      

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

    # show some information on memory consumption of the images
    print("[INFO] features matrix: {:.1f}MB".format(
        data.nbytes / (1024 * 1000.0)))

    # encode the labels as integers
    le = LabelEncoder()
    labels = le.fit_transform(labels)


    # partition the data into training and testing splits using 75% of
    # the data for training and the remaining 25% for testing
    (trainX, testX, trainY, testY) = train_test_split(data, labels,
        test_size=0.25, random_state=42)


    # train and evaluate a k-NN classifier on the raw pixel intensities
    model = kNN_train(trainX, trainY)
    print(classification_report(testY, model.predict(testX),
        target_names=le.classes_))


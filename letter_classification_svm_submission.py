"""


Dataset is taken from: https://archive.ics.uci.edu/ml/datasets/letter+recognition

Remember
--------
1) SVM algorithms are not scale invariant.
"""
import scipy
from sklearn import svm
from sklearn import preprocessing
from termcolor import colored

from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.manifold.t_sne import TSNE

import argparse, os, sys

def get_input_data(filename):
    """
    Function to read the input data from the letter recognition data file.

    Parameters
    ----------
    filename: The path to input data file

    Returns
    -------
    X: The input for the SVM classifier of the shape [n_samples, n_features].
       n_samples is the number of data points (or samples) that are to be loaded.
       n_features is the length of feature vector for each data point (or sample).
    Y: The labels for each of the input data point (or sample). Shape is [n_samples,].

    """

    X = []; Y = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip().split(',')
            Y.append(line[0])
            X.append([float(x) for x in line[1:]])
    X = np.asarray(X); Y = np.asarray(Y)

    

   

    X = preprocessing.scale(X)


   

    return X, Y

def calculate_metrics(predictions, labels):
    """
    Function to calculate the precision, recall and F-1 score.

    Parameters
    ----------
    predictions: The predictions obtained as output from the SVM classifier
    labels: The true label values corresponding to the entries in predictions

    Returns
    -------
    precision: true_positives / (true_positives + false_positives)
    recall: true_positives / (true_positives + false_negatives)
    f1: 2 * (precision * recall) / (precision + recall)
    ===========================================================================
    """

   
    """
    ===========================================================================
    """

    f1 = f1_score(labels, predictions, labels=None, pos_label=1, average='macro', sample_weight=None)
    recall = recall_score(labels, predictions, labels=None, pos_label=1, average='macro', sample_weight=None)
    precision = precision_score(labels, predictions, labels=None, pos_label=1, average='macro', sample_weight=None)

    return precision, recall, f1

def calculate_accuracy(predictions, labels):
    """
    Function to calculate the accuracy for a given set of predictions and
    corresponding labels.

    Parameters
    ----------
    predictions: The predictions obtained as output from the SVM classifier
    labels: The true label values corresponding to the entries in predictions

    Returns
    -------
    accuracy: Fraction of total samples that have correct predictions (same as
    true label)

    """
    return accuracy_score(labels, predictions)

def SVM(train_data,
        train_labels,
        test_data,
        test_labels,
        kernel='rbf'):
    """
    Function to create, train and test the one-vs-all SVM using scikit-learn.

    Parameters
    ----------
    train_data: Numpy ndarray of shape [n_train_samples, n_features]
    train_labels: Numpy ndarray of shape [n_train_samples,]
    test_data: Numpy ndarray of shape [n_test_samples, n_features]
    test_labels: Numpy ndarray of shape [n_test_samples,]
    kernel: linear (default)
            Which kernel to use for the SVM

    Returns
    -------
    accuracy: Accuracy of the model on the test data
    top_predictions: Top predictions for each test sample
    precision: The precision score for the test data
    recall: The recall score for the test data
    f1: The F1-score for the test data

    """

    """
    Create an SVM instance with the required parameters and train it.
    For details on how to do this in scikit-learn, refer:
        http://scikit-learn.org/stable/modules/svm.html
    ==========================================================================
    """

    # YOUR CODE GOES HERE
    C=[]

    clf = svm.SVC(decision_function_shape='ovr',kernel='rbf')
    clf.fit(train_data,train_labels)

    C=clf.predict(train_data)

    """
    ==========================================================================
    """

    """
    Calculates training accuracy. Replace predictions and labels with your
    respective variable names.
    """
    train_accuracy = calculate_accuracy(C, train_labels)
    print "Training Accuracy: %.4f" % (train_accuracy)

    

    D=[]
    D=clf.predict(test_data)

    test_accuracy = calculate_accuracy(D,test_labels)
    print "Test Accuracy: %.4f" %(test_accuracy)

    precision, recall, f1 = calculate_metrics(D,test_labels)

    """
    ==========================================================================
    """

    return test_accuracy, precision, recall, f1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', default=None,
            help='path to the directory containing the dataset file')

    args = parser.parse_args()
    if args.data_dir is None:
        print "Usage: python letter_classification_svm.py --data_dir='<dataset dir path>'"
        sys.exit()
    else:
        filename = os.path.join(args.data_dir, 'letter_classification_train.data')
        try:
            if os.path.exists(filename):
                print "Using %s as the dataset file" % filename
        except:
            print "%s not present in %s. Please enter the correct dataset directory" % (filename, args.data_dir)
            sys.exit()

    # Set the value for svm_kernel as required.
    svm_kernel = 'rbf'

    

    X_data, Y_data = get_input_data(filename)

    """
    ==========================================================================
    """

    """
    We use 5-fold cross validation for reporting the final scores and metrics.
    Code to generate the 5-folds (You can change the split function to something
    else that you like as well) and then calling the SVM to classify the present
    split.
    ==========================================================================
    """
    sss = StratifiedShuffleSplit(n_splits=5, test_size=0.125)   # Do not change this split size
    accumulated_metrics = []
    fold = 1
    for train_indices, test_indices in sss.split(X_data, Y_data):
        print "Fold%d -> Number of training samples: %d | Number of testing "\
            "samples: %d" % (fold, len(train_indices), len(test_indices))
        train_data, test_data = X_data[train_indices], X_data[test_indices]
        train_labels, test_labels = Y_data[train_indices], Y_data[test_indices]
        accumulated_metrics.append(
            SVM(train_data, train_labels, test_data, test_labels,
                svm_kernel))
        fold += 1

    """
    ==========================================================================
    """
    
    for i in range (0,len(accumulated_metrics)):
    	print '\nFold '+ str(i) + '\n' 
    	text = colored('Accuracy,Precision,Recall,f1 score values from the accumulates metrics are ', 'blue', attrs=['blink']) 
    	print text
    	print accumulated_metrics[i]

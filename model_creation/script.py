import os
from os.path import isfile
import pandas as pd
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import cross_val_score

def get_directories_in(path='.'):
    directories = []
    files = os.listdir(path)
    for file in files:
        if not isfile(file) and not file.startswith('.'):
            directories.append(f"{path}/{file}")
    return directories

def get_images_in(directory):
    img_list = []
    files = os.listdir(directory)
    for file in files:
        if isfile(os.path.join(directory, file)) and file.endswith('.jpg'):
            img_list.append(Image.open(os.path.join(directory, file)))
    return img_list

def cross_validate_model(model, X, y, cv=5):
    """
    Perform cross-validation on the model using the given features and labels.
    
    Args:
        model: The machine learning model to evaluate
        X: Feature data
        y: Label data
        cv: Number of cross-validation folds

    Returns:
        A list of cross-validation scores
    """
    scores = cross_val_score(model, X, y, cv=cv)
    return scores

def evaluate_model_performance(model, X_train, X_test, y_train, y_test):
    """
    Evaluate the performance of the model using various metrics.

    Args:
        model: The machine learning model to evaluate
        X_train: Training feature data
        X_test: Testing feature data
        y_train: Training label data
        y_test: Testing label data

    Returns:
        A dictionary containing various performance metrics
    """
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)

    performance_metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='weighted'),
        'recall': recall_score(y_test, y_pred, average='weighted'),
        'f1_score': f1_score(y_test, y_pred, average='weighted')
    }
    return performance_metrics
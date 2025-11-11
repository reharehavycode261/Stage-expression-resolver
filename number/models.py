import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score

def cross_validate(model, X, y, cv=5):
    """
    Effectue la validation croisée avec les données et un modèle donné.
    
    :param model: Le modèle à valider.
    :param X: Les caractéristiques d'entrée.
    :param y: Les étiquettes de sortie.
    :param cv: Nombre de folds pour la validation croisée.
    :return: Liste des scores de validation croisée.
    """
    kf = KFold(n_splits=cv, shuffle=True, random_state=42)
    scores = []

    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        score = accuracy_score(y_test, predictions)
        scores.append(score)

    return scores

def evaluate_model_performance(scores):
    """
    Évalue la performance du modèle basé sur les scores de validation croisée.
    
    :param scores: Liste des scores obtenus durant la validation croisée.
    :return: Dictionnaire avec la moyenne et l'écart-type des scores.
    """
    return {
        'mean_accuracy': np.mean(scores),
        'std_accuracy': np.std(scores)
    }
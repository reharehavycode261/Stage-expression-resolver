import numpy as np
from django.http import JsonResponse
from sklearn.dummy import DummyClassifier
from number.models import cross_validate, evaluate_model_performance

def perform_cross_validation(request):
    """
    Vue effectuant la validation croisée sur le modèle et retournant ses scores.
    """
    # Exemple de données d'entraînement
    X = np.array([[1], [2], [3], [4], [5]])  # Remplacez par vos véritables caractéristiques
    y = np.array([0, 1, 0, 1, 0])  # Remplacez par vos véritables labels

    # Utilisation d'un DummyClassifier pour l'exemple
    model = DummyClassifier(strategy="most_frequent")

    # Exécuter la validation croisée
    scores = cross_validate(model, X, y, cv=5)
    performance = evaluate_model_performance(scores)

    return JsonResponse(performance)
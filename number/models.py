import numpy as np
import pandas as pd
from django.db import models

class Anomaly(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Anomaly(id={self.id}, resolved={self.is_resolved})"

# Modèle existant pour référence
class Character(models.Model):
    # Supposons que ce modèle existe déjà
    # Exemple de champs pour contexte
    name = models.CharField(max_length=100)
    detected_anomalies = models.ManyToManyField(Anomaly, related_name="characters")
    # Autres champs et méthodes...
import operator
import pickle
import numpy as np
import pandas as pd
from PIL import Image
from django.db import models
from sympy import symbols
from number.expression import calculate, separation

def load(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def opposite(x):
    if x == '-':
        return '+'
    elif x == '+':
        return '-'
    elif x == '*':
        return '/'
    elif x == '/':
        return '*'
    else:
        return None

class NumberData(models.Model):
    value = models.FloatField()
    detected_anomaly = models.BooleanField(default=False)
    anomaly_reason = models.CharField(max_length=255, null=True, blank=True)

    def check_for_anomalies(self):
        # Logique simplifiée de détection d'anomalies
        if self.value > 1000 or self.value < -1000:  # exemple simple de plage d'anomalies
            self.detected_anomaly = True
            self.anomaly_reason = "Valeur hors de la plage normale"
            self.save()
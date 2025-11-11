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
    return None

class AnomalyOutlier(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    severity = models.IntegerField(default=0)  # scale of severity
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
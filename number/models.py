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
        return '+'


class Character(models.Model):
    MODEL = load('./model_creation/model.pickle')
    image = models.ImageField(null=True)
    prediction = models.CharField(null=True, max_length=1)
    correct = models.CharField(null=True, max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def split_image_col(image):
        image = np.array(image)
        image_split = []
        temp = []
        for i in range(0, image.shape[1]):
            if image[:, i].mean() == 255:
                if i - 1 > 0 and image[:, i - 1].mean() != 255:
                    image_split.append(np.transpose(np.array(temp)))
                    temp = []
            else:
                temp.append(image[:, i])
        if len(temp) > 0:
            image_split.append(temp)
        return image_split

    @staticmethod
    def split_image_row(image):
        image = image.convert('L')
        image = np.array(image)
        image = np.where(image > 0, 255, 0)
        image_split = []
        temp = []
        for i in range(0, image.shape[0]):
            if image[i].mean() == 255:
                if i - 1 > 0 and image[i - 1].mean() != 255:
                    image_split.append(Image.fromarray(np.array(temp, dtype='uint8')))
                    temp = []
            else:
                temp.append(image[i, :])
        if len(temp) > 0:
            image_split.append(Image.fromarray(np.array(temp, dtype='uint8')))
        return image_split

    @staticmethod
    def split_image(image):
        rows = Character.split_image_row(image)
        images = []
        for row in rows:
            cols = Character.split_image_col(row)
            for col in cols:
                images.append(Character.rescale_image(col))
        return images

    @staticmethod
    def rescale_image(image):
        non_empty_rows = np.where(np.mean(image, axis=1) < 255)[0]
        image = image[non_empty_rows]

        non_empty_columns = np.where(np.mean(image, axis=0) < 255)[0]
        image = image[:, non_empty_columns]

        image = np.uint8(image)
        image = Image.fromarray(image)

        resized_image = image.resize((28, 28), resample=Image.LANCZOS)
        return np.where(np.array(resized_image) > 50, 255, 0)

    @staticmethod
    def convert_1d(array2d):
        columns = [f'0.' + str(i) for i in range(1, 785)]
        array = [np.ravel(array2d)]
        return pd.DataFrame(array, columns=columns)

    def get_prediction(self):
        image = Image.open(self.image)
        images = Character.split_image(image)
        predictions = []
        for image in images:
            image = Character.convert_1d(image)
            prediction = chr(int(Character.MODEL.predict(image)[0]))
            predictions.append(prediction)
        return predictions

    def get_prediction_str(self):
        pred = self.get_prediction()
        res = ''
        for i, x in enumerate(pred):
            res += x + ' '
        return res.strip().replace('% % %', '>').replace('% %', '<')\
            .replace('w', 'x').replace('%', '=').replace('[', '(').replace(']', ')')

    @staticmethod
    def finalize(equation, sep):
        eq = equation.split(sep)[0][:-2]
        eq = eq+'1' if len(eq) <= 1 else eq
        return equation.split(sep)[1].replace('x', '') + " / " + str(eq).replace('x', '')

    @staticmethod
    def evaluate_expression(expression, x):
        operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '%': operator.mod,
            '**': operator.pow
        }

        stack = []
        tokens = expression.split()

        for token in tokens:
            if token.isdigit():
                stack.append(float(token))
            elif token.isalpha() and token == 'x':
                stack.append(x)
            elif token in operators:
                operand2 = stack.pop()
                operand1 = stack.pop()
                result = operators[token](operand1, operand2)
                stack.append(result)
            else:
                print(f"Opérateur ou variable inconnu : {token}")
                return None

        if len(stack) == 1:
            return stack[0]
        else:
            print("Erreur d'expression.")
            return None

    @staticmethod
    def separation(mot):
        if str(mot).find('>') != -1:
            return '>'
        elif str(mot).find('<') != -1:
            return '<'
        else:
            return '='

    def get_solution(self):
        try:
            sep = self.separation(self.get_prediction_str())
            print(sep)
            equation = self.get_prediction_str().split(sep)
            print('eq:' + str(equation))

            step = ["--> Résolvons l'équation", str(equation[0]) + f' {sep} ' + str(equation[1]),
                    "<br>--> Simplifier l'équation"]

            simpl = str(calculate(equation[0])) + f' {sep} ' + str(calculate(equation[1]))
            print(simpl)
            step.append(simpl)

            step.append("<br>--> Changement de membre")
            change = separation(simpl, sep)
            print("qsdf" + change)
            step.append(change)

            step.append("<br>--> Calcul")
            eq = change.split(sep)
            mem1 = calculate(eq[0])
            mem2 = calculate(eq[1])
            eq = str(mem1) + f' {sep} ' + str(mem2)
            step.append(eq)
            print('eto1 -->' + eq)
            step.append(f"x {sep} "+self.finalize(eq, sep))
            print(f"eto2 --> x {sep} "+self.finalize(eq, sep))

            res = calculate(self.finalize(eq, sep))
            step.append(f"x {sep} " + res)
            print('eto3')

            return step, res, sep
        except Exception as e:
            # raise e
            return ["Il n'y a pas de résultat!"], None, None

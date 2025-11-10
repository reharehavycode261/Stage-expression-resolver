import pickle
from io import BytesIO

from PIL import Image
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render

from S4_IA.settings import BASE_DIR
from number.models import Character


def index(request):
    if request.method == 'POST':
        c = Character.objects.create(image=request.FILES.get('image'))
        print(c.get_prediction())
        step, res, sep = c.get_solution()
        return JsonResponse({
            'pred_recu': ' '.join(c.get_prediction()),
            'pred_convert': c.get_prediction_str(),
            'prediction': step,
            'res_equ': res,
            'sep_equ': sep
        })
    return render(request, 'index.html')

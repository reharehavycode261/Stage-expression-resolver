import pickle
from io import BytesIO
from PIL import Image
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from S4_IA.settings import BASE_DIR
from number.models import Character, AnomalyOutlier

def index(request):
    if request.method == 'POST':
        c = Character.objects.create(image=request.FILES.get('image'))
        print(c.get_prediction())
        step, res, sep = c.get_solution()
        return JsonResponse({
            'steps': step,
            'result': res,
            'separation': sep
        })

def anomaly_list(request):
    anomalies = AnomalyOutlier.objects.filter(active=True)
    return render(request, 'number/anomaly_list.html', {'anomalies': anomalies})

def anomaly_detail(request, pk):
    anomaly = get_object_or_404(AnomalyOutlier, pk=pk)
    return render(request, 'number/anomaly_detail.html', {'anomaly': anomaly})
from django.shortcuts import render
from .models import NumberData

def index(request):
    numbers = NumberData.objects.all()
    for number in numbers:
        number.check_for_anomalies()
    context = {'numbers': numbers}
    return render(request, 'number/index.html', context)
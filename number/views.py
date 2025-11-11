import json
import numpy as np
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
import base64

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def visualize_equation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        equation = data['equation']
        x = np.linspace(-10, 10, 400)
        try:
            y = eval(equation)  # Evaluates the equation directly but CAUTION: this is unsafe!
            fig, ax = plt.subplots()
            ax.plot(x, y)
            ax.set(title='Graph of {}'.format(equation), xlabel='x', ylabel='f(x)')
            buf = BytesIO()
            plt.savefig(buf, format='png')
            plt.close(fig)
            buf.seek(0)
            return HttpResponse('data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode(), content_type="text")
        except Exception as e:
            return HttpResponse(status=400, content=str(e))
    return HttpResponse(status=405)
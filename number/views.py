import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render

def plot_equation_view(request):
    if request.method == "POST":
        equation = request.POST.get('equation', 'x**2')  # Par défaut une parabole si non spécifiée
        x = np.linspace(-10, 10, 400)
        y = eval(equation, {"x": x, "np": np})

        plt.figure()
        plt.plot(x, y)
        plt.title(f'Graph of {equation}')
        plt.xlabel('x')
        plt.ylabel('y')

        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return HttpResponse(buf.read(), content_type='image/png')

    return render(request, 'index.html')
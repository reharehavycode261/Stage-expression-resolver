from django.shortcuts import render
import numpy as np
import matplotlib.pyplot as plt
import io
import urllib, base64

def plot_equation(request):
    plot = None
    if request.method == 'POST':
        equation = request.POST.get('equation', '')

        # Convertir l'équation pour utilisation par numpy
        x = np.linspace(-10, 10, 400)
        y = eval(equation, {'x': x, 'np': np})

        # Création de la figure
        plt.figure()
        plt.plot(x, y, label=equation)
        plt.title('Visualisation de l\'équation')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.axhline(0, color='black',linewidth=0.5)
        plt.axvline(0, color='black',linewidth=0.5)
        plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
        plt.legend()

        # Conversion de la figure en image PNG
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        plot = urllib.parse.quote(string)

    return render(request, 'index.html', {'plot': plot})
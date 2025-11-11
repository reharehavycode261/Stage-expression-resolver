from django.urls import path
from . import views

urlpatterns = [
    path('plot-equation/', views.plot_equation_view, name='plot_equation'),
]
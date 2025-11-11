from django.urls import path
from . import views

urlpatterns = [
    path('plot/', views.plot_equation, name='plot_equation'),
]
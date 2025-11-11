from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('anomalies/', views.anomaly_list, name='anomaly_list'),
    path('anomalies/<int:pk>/', views.anomaly_detail, name='anomaly_detail'),
]
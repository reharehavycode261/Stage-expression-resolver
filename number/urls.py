from django.urls import path

from number import views

urlpatterns = [
    path('', views.index, name='number_index'),
    # path('correction', views.correction, name='number_correction'),
    # path('admin/', admin.site.urls),
]

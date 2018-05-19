from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.saisie_vol2, name='saisie_vol2'),
]

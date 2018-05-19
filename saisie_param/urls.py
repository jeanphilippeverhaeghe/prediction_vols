from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.saisie_param, name='saisie_param'),
    path('', views.saisie_param, name='show_param'),
]

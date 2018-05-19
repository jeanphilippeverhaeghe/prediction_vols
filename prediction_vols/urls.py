from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.saisie_vol, name='saisie_vol'),
]

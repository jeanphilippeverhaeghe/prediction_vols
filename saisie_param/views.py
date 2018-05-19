from django.shortcuts import render

# Create your views here.
from .forms import SaisieParamForm
from .models import Parametres


def saisie_param(request):
    # Construire le formulaire, avec les données postées,
    # soit vide si l'utilisateur accède pour la première fois
    # à la page.
    form = SaisieParamForm(request.POST or None)
    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données 
    # dans le formulaire ou qu'il contient des erreurs.
    if form.is_valid(): 
        # Ici nous pouvons traiter les données du formulaire
        ridge_param = form.cleaned_data['ridge_param']
        ridge_coef = form.cleaned_data['ridge_coef']
        ridge_intercep = form.cleaned_data['ridge_intercep']
        p = Parametres()
        p.param = ridge_param
        p.coef = ridge_coef
        p.intercept = str(ridge_intercep)
        p.save()
        
        print ("ridge_param: " ,ridge_param)
        print ("ridge_coef: ",ridge_coef)
        print ("ridge_intercep: ", ridge_intercep+1)

    
    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'saisie_param.html', locals())


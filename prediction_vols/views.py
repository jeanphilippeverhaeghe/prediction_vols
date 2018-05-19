from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')

from .forms import SaisieVolForm

def saisie_vol(request):
    # Construire le formulaire, avec les données postées,
    # soit vide si l'utilisateur accède pour la première fois
    # à la page.
    form = SaisieVolForm(request.POST or None)
    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données 
    # dans le formulaire ou qu'il contient des erreurs.
    if form.is_valid(): 
        # Ici nous pouvons traiter les données du formulaire
        Aeroport_dep = form.cleaned_data['Aeroport_dep']
        Aeroport_arr = form.cleaned_data['Aeroport_arr']
        Compagnie = form.cleaned_data['Compagnie']
        MoisDep = form.cleaned_data['MoisDep']
        JourDep = form.cleaned_data['JourDep']
        JourSemaine = form.cleaned_data['JourSemaine']
        HeureDep = form.cleaned_data['HeureDep']
        HeureArr = form.cleaned_data['HeureArr']

        # Nous pourrions ici envoyer l'e-mail grâce aux données 
        # que nous venons de récupérer
        print ("Code Compagnie: " ,Compagnie[0])
        print ("Code Jour_Semaine: ",JourSemaine[0])
        print ("Code Aeroport_dep: ",Aeroport_dep)
        print ("Code MoisDep: ",MoisDep)
        print ("Code HeureDep: ",HeureDep)
        print ("Code HeureArr: ",HeureArr)

        from . import Airport_Delay_V0
        pred, comment_pred = Airport_Delay_V0.prediction(origin = Aeroport_dep, destination = Aeroport_arr,
            carrier = Compagnie[0], dept_time = HeureDep, arr_time = HeureArr,
            month = MoisDep, day = JourDep, weekday = JourSemaine[0])

        form.fields['Prediction'].label="Prédiction du retard de votre vol (en min): " + str(pred)
        form.fields['Comment_Prediction'].label="Commentaire sur la prédiction: " + comment_pred
    
    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'saisie_vol.html', locals())



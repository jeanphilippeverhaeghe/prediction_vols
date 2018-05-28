from django.shortcuts import render

import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from saisie_param.models import Parametres

# Create your views here.

from .forms import SaisieVolForm2

def saisie_vol2(request):
    # Construire le formulaire
    form = SaisieVolForm2(request.POST or None)
    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données
    # dans le formulaire ou qu'il contient des erreurs.
    if form.is_valid():
        # Ici nous pouvons traiter les données du formulaire
        carrier_delay = form.cleaned_data['CARRIER_DELAY']
        weather_delay = form.cleaned_data['WEATHER_DELAY']
        nas_delay = form.cleaned_data['NAS_DELAY']
        security_delay = form.cleaned_data['SECURITY_DELAY']
        late_aircraft_delay = form.cleaned_data['LATE_AIRCRAFT_DELAY']
        distance = form.cleaned_data['DISTANCE']
        air_time = form.cleaned_data['AIR_TIME']
        crs_elapsed_time = form.cleaned_data['CRS_ELAPSED_TIME']
        actual_elapsed_time = form.cleaned_data['ACTUAL_ELAPSED_TIME']

        Aeroport_dep = form.cleaned_data['Aeroport_dep']
        Aeroport_arr = form.cleaned_data['Aeroport_arr']
        Compagnie=[]
        Compagnie = form.cleaned_data['Compagnie']
        MoisDep = form.cleaned_data['MoisDep']
        #JourDep = form.cleaned_data['JourDep']
        JourSemaine=[]
        JourSemaine = form.cleaned_data['JourSemaine']
        #HeureDep = form.cleaned_data['HeureDep']
        #HeureArr = form.cleaned_data['HeureArr']

        # Traitement
        print ("carrier_delay: ",carrier_delay)
        print ("weather_delay : ",weather_delay)
        print ("nas_delay : ",nas_delay)
        print ("security_delay : ",security_delay)
        print ("late_aircraft_delay : ",late_aircraft_delay)
        print ("distance : ",distance)
        print ("air_time : ",air_time)
        print ("crs_elapsed_time : ",crs_elapsed_time)
        print ("actual_elapsed_time : ",actual_elapsed_time)
        print ("Code Compagnie: " ,Compagnie)
        print ("Code Aeroport_dep: ",Aeroport_dep)
        print ("Code Aeroport_arr: ",Aeroport_arr)
        print ("Code MoisDep: ",MoisDep)
        #print ("Code JourDep: ",JourDep)
        print ("Code Jour_Semaine: ",JourSemaine)
        #print ("Code HeureDep: ",HeureDep)

        #extraction des parametres de la Base de données:
        #Version pour Ridge
        q1= Parametres.objects.filter(id=2).values('param','coef','intercept')
        param = eval((q1.values_list("param")[0])[0])   #il me faut un class 'dict'
        coef = np.array((q1.values_list("coef")[0])[0]) #il me faut un class 'numpy.ndarray'
        intercept = q1.values_list("intercept")[0][0] #il me faut un class 'numpy.float64'
        intercept = np.float64(intercept)

        #je n'arrive pas à obtenir en lisant la base de données un numpy.ndarray de float ! Je me le code en dur ! ZUT !
        coef = np.float_([1.16964376,1.08054175,0.6773621,1.16804885,1.17066624,0.0037279,0.05143339,-0.70899413,0.6302446])

        #Version pour RFC
        #q2= Parametres.objects.filter(id=3).values('param')
        #param = eval((q2.values_list("param")[0])[0])   #il me faut un class 'dict'
        print("param: ", param)
        print (type(param))
        print("coef: ", coef)
        print (type(coef))
        print("intercept: ", intercept)
        print(type(intercept))


        #Prédiction sans matrice ni fit:
        ar = np.array([[carrier_delay,weather_delay,nas_delay,security_delay,late_aircraft_delay,distance,
                        air_time,crs_elapsed_time,actual_elapsed_time]])
        df = pd.DataFrame(ar, index = [1], columns = ['CARRIER_DELAY','WEATHER_DELAY', 'NAS_DELAY',
                        'SECURITY_DELAY','LATE_AIRCRAFT_DELAY','DISTANCE','AIR_TIME','CRS_ELAPSED_TIME',
                        'ACTUAL_ELAPSED_TIME'])
        #Version Ridge:
        new_ridge= linear_model.Ridge(alpha=100)
        new_ridge.set_params = param
        new_ridge.coef_ = coef
        new_ridge.intercept_= intercept
        nouvelle_prediction = new_ridge.predict(df)
        pred = float(nouvelle_prediction)
        comment_pred = "Prédiction à base des coef de la régression, sans matrice ni FIT"
        
        #Version RFC:
        #new_rfc = RandomForestRegressor()
        #new_rfc.set_params = param
        #new_rfc.estimators_= intercept
        #nouvelle_prediction = new_rfc.predict(df)
        #pred = float(nouvelle_prediction)
        #comment_pred = "Prédiction à base des coef de la régression Random Forest Regressor, sans matrice ni FIT"
        
        
        print("nouvelle_prediction: ", nouvelle_prediction)

        form.fields['Prediction'].label="Prédiction de l'avance/retard de votre vol (en min): " + str(round(pred,2))
        form.fields['Comment_Prediction'].label="Commentaire sur la prédiction: " + comment_pred



        ########################
        #Prédiction plus précise
        ########################
        #Si au moins un des paramêtres de précision est non nul, on peut lancer un nouveau Ridge
        if len(Compagnie) != 0 or len(JourSemaine) != 0 or Aeroport_dep !='' or Aeroport_arr !='' :
            if len(Compagnie) == 0:
                compa = ''
            else:
                compa = Compagnie[0]

            if len(JourSemaine) == 0:
                JourS = 0
            else:
                JourS = int(JourSemaine[0])

            #Version Ridge
            from . import Airport_Delay_V1
            pred, comment_pred = Airport_Delay_V1.prediction2(param = param, coef = coef, intercept = intercept, origin = Aeroport_dep,
                destination = Aeroport_arr, carrier = compa, month = MoisDep, weekday = JourS)

            #Version Random Forest 
            #from . import Airport_Delay_V2
            #pred, comment_pred = Airport_Delay_V2.prediction2(param = param, estimators = intercept, origin = Aeroport_dep,
            #    destination = Aeroport_arr, carrier = compa, month = MoisDep, weekday = JourS)


            form.fields['Prediction'].label="Prédiction de l'avance/retard de votre vol (en min): " + str(round(pred,2))
            form.fields['Comment_Prediction'].label="Commentaire sur la prédiction (plus précise): " + comment_pred


    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'saisie_vol2.html', locals())

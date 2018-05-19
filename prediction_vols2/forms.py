from django import forms

jour_semaine2 = ((1,'Lundi'),(2,'Mardi'),(3,'Mercredi'),(4,'Jeudi'),(5,'Vendredi'),(6,'Samedi'),(7,'Dimanche'))
cie_aerienne2 = (
('FL','AirTran airways'),
('AS','Alaska airlines'),
('AA','American airlines'), 
('DL','Delta airways'),
('9E','Endeavor air'),
('MQ','Envoy air'),
('EV','ExpressJet airlines'),
('F9','Frontier airlines'),
('HA','Hawaiian airlines'),
('B6','JetBlue airways'),
('YV','Mesa airlines'),
('OO','SkyWest airlines'),
('WN','Southwest airlines'),
('NK','Spirit airlines'),
('UA','United airlines'),
('US','US airways'),
('VX','Virgin America')
)

class SaisieVolForm2(forms.Form):
    CARRIER_DELAY = forms.IntegerField(label= "Carrier delay (min)", min_value=0, max_value=600)
    WEATHER_DELAY = forms.IntegerField(label= "Weather delay (min)", min_value=0, max_value=600)
    NAS_DELAY = forms.IntegerField(label= "NAS delay (min)", min_value=0, max_value=600)
    SECURITY_DELAY = forms.IntegerField(label= "Security delay (min)", min_value=0, max_value=600)
    LATE_AIRCRAFT_DELAY = forms.IntegerField(label= "Late aircraft delay (min)", min_value=0, max_value=600)
    DISTANCE = forms.IntegerField(label= "Distance (milles)", min_value=1, max_value=100000)
    AIR_TIME = forms.IntegerField(label= "Air time (min)", min_value=0, max_value=1200)
    CRS_ELAPSED_TIME = forms.IntegerField(label= "Scheduled elapsed time (min)", min_value=0, max_value=1200)
    ACTUAL_ELAPSED_TIME = forms.IntegerField(label= "Actual elapsed time (min)", min_value=0, max_value=1200)


    Aeroport_dep = forms.CharField(label="Aéroport d'origine",max_length=100,required=False)
    Aeroport_arr = forms.CharField(label="Aéroport d'arrivée",max_length=100,required=False)
    Compagnie = forms.MultipleChoiceField(label = "Compagnie Aérienne", required = False, widget=forms.SelectMultiple, choices = cie_aerienne2,)
    JourSemaine = forms.MultipleChoiceField(label = "Jour de la semaine", required = False, widget=forms.SelectMultiple, choices = jour_semaine2,)
    #JourDep = forms.IntegerField(label= "Jour du mois", min_value=1, max_value=31,required=False)
    MoisDep = forms.IntegerField(label= "Mois", min_value=1, max_value=12,required=False)
    #HeureDep = forms.IntegerField(label= "Heure (de départ)", min_value=0, max_value=23,required=False)
    #HeureArr = forms.IntegerField(label= "Heure (d'arrivée)", min_value=0, max_value=23,required=False)
    
    Prediction = forms.BooleanField(label="Prédiction du retard de votre vol (en min) ==> ", required = False, disabled= True)
    Comment_Prediction = forms.BooleanField(label="Commentaire sur la prédiction", required = False, disabled= True)
    def __str__(self):
        return self.titre


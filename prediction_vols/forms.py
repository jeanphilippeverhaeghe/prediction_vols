from django import forms

jour_semaine = ((1,'Lundi'),(2,'Mardi'),(3,'Mercredi'),(4,'Jeudi'),(5,'Vendredi'),(6,'Samedi'),(7,'Dimanche'))
cie_aerienne = (
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

class SaisieVolForm(forms.Form):
    Aeroport_dep = forms.CharField(label="Aéroport d'origine",max_length=100)
    Aeroport_arr = forms.CharField(label="Aéroport d'arrivée",max_length=100)
    #Compagnie = forms.CharField(label="Compagnie Aérienne",max_length=100)
    Compagnie = forms.MultipleChoiceField(label = "Compagnie Aérienne", required = True, widget=forms.SelectMultiple, choices = cie_aerienne,)
    JourSemaine = forms.MultipleChoiceField(label = "Jour de la semaine", required = True, widget=forms.SelectMultiple, choices = jour_semaine,)
    JourDep = forms.IntegerField(label= "Jour du mois", min_value=1, max_value=31)
    MoisDep = forms.IntegerField(label= "Mois", min_value=1, max_value=12)
    HeureDep = forms.IntegerField(label= "Heure (de départ)", min_value=0, max_value=23)
    HeureArr = forms.IntegerField(label= "Heure (d'arrivée)", min_value=0, max_value=23)
    
    Prediction = forms.BooleanField(label="Prédiction du retard de votre vol (en min) ==> ", required = False, disabled= True)
    Comment_Prediction = forms.BooleanField(label="Commentaire sur la prédiction", required = False, disabled= True)
    def __str__(self):
        return self.titre


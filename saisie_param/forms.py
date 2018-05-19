from django import forms



class SaisieParamForm(forms.Form):
    ridge_param = forms.CharField(label="Parametres de la régression Ridge",max_length=1000)
    ridge_coef = forms.CharField(label="Coefficients de la régression Ridge",max_length=1000)
    ridge_intercep = forms.FloatField(label= "Coef Intercept de la régression Ridge")
    def __str__(self):
        return self.titre


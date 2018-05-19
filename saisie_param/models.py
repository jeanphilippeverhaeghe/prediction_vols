from django.db import models

# Create your models here.
class Parametres(models.Model):
    param = models.CharField(max_length = 1000)
    coef = models.CharField(max_length = 1000)
    intercept = models.CharField(max_length = 1000)
    def __str__(self):
        return self.param

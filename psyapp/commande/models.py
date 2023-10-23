from django.db import models
from accounts.models import Psy



class Specialisation(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.nom


class Panier(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    specialisations = models.ManyToManyField(Specialisation, related_name='paniers')

    def __str__(self):
        return self.nom

<<<<<<< HEAD
class SpecialisteChoisi(models.Model):
    psy = models.ForeignKey(Psy, on_delete=models.CASCADE, related_name='specialistes_choisis')
=======

class Specialiste(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
>>>>>>> bca8d6680dd0be136c0973f784e3512e1b259003
    specialisations = models.ManyToManyField(Specialisation, related_name='specialistes')
    paniers = models.ManyToManyField(Panier, related_name='specialistes')

    def __str__(self):
        return f"{self.psy.prenom} {self.psy.nom}"

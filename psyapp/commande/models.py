from django.db import models


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


class Specialiste(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    specialisations = models.ManyToManyField(Specialisation, related_name='specialistes')
    paniers = models.ManyToManyField(Panier, related_name='specialistes')

    def __str__(self):
        return f"{self.prenom} {self.nom}"

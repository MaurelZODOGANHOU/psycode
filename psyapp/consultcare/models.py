from django.db import models

from accounts.models import User


# Create your models here.

class TypeConsultation(models.Model):
    type_name = models.CharField(max_length=50, unique=True, choices=[
        ('In-Office', 'In-Office'),
        ('Video', 'Video'),
        ('Audio', 'Audio'),
        ('Chat', 'Chat')
    ])

    def __str__(self):
        return self.type_name


class Psy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    adresse_residence = models.CharField(max_length=255)
    type_consultation = models.ForeignKey(TypeConsultation, on_delete=models.SET_NULL, null=True)
    numero_ordre = models.CharField(max_length=255)
    pays_obtention = models.CharField(max_length=255)
    diplome = models.CharField(max_length=255)
    cabinet = models.ForeignKey('Cabinet', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class LieuConsultation(models.Model):
    adresse = models.CharField(max_length=255)
    telephone_professionnel = models.CharField(max_length=15)
    consultant = models.OneToOneField(Psy, on_delete=models.CASCADE, related_name='lieu')

    def __str__(self):
        return self.adresse


class Cabinet(models.Model):
    nom_cabinet = models.CharField(max_length=255)
    nom_legal = models.CharField(max_length=255)
    statut_juridique = models.CharField(max_length=255)
    adresse_cabinet = models.CharField(max_length=255)
    IFU_Siret_EIN = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.nom_cabinet

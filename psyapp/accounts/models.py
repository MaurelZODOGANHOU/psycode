from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'adresse e-mail est obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('Patient', 'Patient'),
        ('Psy', 'Psy'),
    )
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255)
    date_naissance = models.DateField()
    telephone = PhoneNumberField()
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'date_naissance', 'telephone', 'user_type']

    def __str__(self):
        return self.username


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
    telephone = PhoneNumberField()
    email = models.EmailField()

    def __str__(self):
        return self.nom_cabinet

    def validate_professional_email(value):
        banned_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
        if any(domain in value for domain in banned_domains):
            raise ValidationError("Veuillez utiliser un e-mail professionnel.")


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

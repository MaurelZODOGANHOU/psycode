from datetime import timedelta
from accounts.models import Psy, Patient
from django.db.models.signals import pre_save
from django.dispatch import receiver

from zoomapp.models import AppelClientTwilio, VideoCall, EmailConsultation, SmsMessages
from django.db import models
from django.conf import settings
import stripe


class SpecialisationPsy(models.Model):
    psy = models.ForeignKey(Psy, on_delete=models.CASCADE)
    specialist = models.CharField(max_length=50, choices=[
        ('Psychologue', 'Psychologue'),
        ('Psychiatre', 'Psychiatre'),
        ('Psychotherapeute', 'Psychotherapeute'),
        ('Psychanalyste', 'Psychanalyste')
    ])


class ForfaitConsultation(models.Model):
    psy = models.ForeignKey(Psy, on_delete=models.CASCADE, related_name='forfaits')
    nom = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    duree = models.IntegerField(help_text="Durée du forfait en jours")
    nombre_consultations = models.IntegerField(help_text="Nombre de consultations incluses dans le forfait")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom} - {self.psy}"


class SouscriptionForfait(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="souscriptions")
    forfait = models.ForeignKey(ForfaitConsultation, on_delete=models.CASCADE, related_name="souscriptions")
    date_souscription = models.DateTimeField(auto_now_add=True)
    date_expiration = models.DateTimeField()
    consultations_restantes = models.IntegerField()

    def __str__(self):
        return f"{self.patient} - {self.forfait} - {self.consultations_restantes} consultations restantes"


class Consultation(models.Model):
    COMMUNICATION_CHOICES = [
        ('SMS', 'Messagerie SMS'),
        ('AudioCall', 'Appel Audio'),
        ('VideoCall', 'Appel Vidéo'),
        ('Email', 'Email'),
        ('Office', 'Office'),

    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    souscription = models.ForeignKey(SouscriptionForfait, on_delete=models.CASCADE, related_name='consultations')
    psy = models.ForeignKey(Psy, on_delete=models.CASCADE)
    communication_method = models.CharField(max_length=10, choices=COMMUNICATION_CHOICES)
    date_et_heure = models.DateTimeField()
    duree = models.DurationField(default=timedelta(minutes=30))  # durée par défaut de 30 minutes

    status = models.CharField(max_length=20,
                              choices=[('planifiee', 'Planifiée'), ('en_cours', 'En cours'), ('terminee', 'Terminée'),
                                       ('annulee', 'Annulée')], default='planifiee')
    note = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.create_communication_instance()

    def create_communication_instance(self):
        if self.communication_method == 'SMS':
            self.create_sms()
        elif self.communication_method == 'AudioCall':
            self.create_audio_call()
        elif self.communication_method == 'VideoCall':
            self.create_video_call()
        elif self.communication_method == 'Email':
            self.create_email_consultation()
        else:
            raise ValueError("Méthode de communication non prise en charge")

    def create_sms(self):
        # Assurez-vous d'avoir tous les champs nécessaires pour créer un SmsMessages
        SmsMessages.objects.create(recipient=self.patient, sender=self.psy, corps="Votre message ici")

    def create_audio_call(self):
        # Assurez-vous d'avoir tous les champs nécessaires pour créer un AppelClientTwilio
        AppelClientTwilio.objects.create(calling_from=self.psy, calling_receive=self.patient,
                                         url_twilio_demo="URL de votre audio")

    def create_video_call(self):
        # Assurez-vous d'avoir tous les champs nécessaires pour créer un VideoCall
        VideoCall.objects.create(patient=self.patient, psy=self.psy, room_sid="Votre SID de salle")

    def create_email_consultation(self):
        # Assurez-vous d'avoir tous les champs nécessaires pour créer un EmailConsultation
        EmailConsultation.objects.create(patient=self.patient, psy=self.psy, subject="Votre sujet",
                                         message="Votre message")

    def __str__(self):
        return f"{self.psy} - {self.patient} - {self.communication_method}"


stripe.api_key = settings.STRIPE_SECRET_KEY


class Commande(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='commandes')
    psy = models.ForeignKey(Psy, on_delete=models.CASCADE)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, default='en_attente')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.stripe_payment_intent_id and self.total:
            # Créer un PaymentIntent Stripe
            payment_intent = stripe.PaymentIntent.create(
                amount=int(self.total * 100),  # Montant en centimes
                currency='eur',
                payment_method_types=['card'],
            )
            self.stripe_payment_intent_id = payment_intent['id']

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Commande de {self.patient} avec {self.psy}"


@receiver(pre_save, sender=Commande)
def set_commande_total(sender, instance, **kwargs):
    if instance.consultation and instance.consultation.souscription:
        instance.total = instance.consultation.souscription.forfait.prix

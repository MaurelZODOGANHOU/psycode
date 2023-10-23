from django.db import models
from twilio.rest import Client

from accounts.models import Patient, Psy

from django.db import models
from twilio.rest import Client

"""
class Communication(models.Model):
    TYPE_CHOICES = [
        ('sms', 'SMS'),
        ('call', 'Appel'),
        ('video', 'Vidéo'),
    ]

    sender = models.ForeignKey(Psy, on_delete=models.CASCADE, related_name='communications_sent')
    recipient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='communications_received')
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    content = models.TextField(max_length=160, blank=True, null=True)
    url_twilio_demo = models.URLField(blank=True, null=True)
    room_sid = models.CharField(max_length=34, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('ongoing', 'Ongoing'), ('finished', 'Finished')], default='pending', blank=True, null=True)

    def __str__(self):
        return f"{self.sender.user.username} -> {self.recipient.user.username} : {self.get_type_display()}"

    def save(self, *args, **kwargs):
        account_sid = 'AC3330ae3a0049673de9c3e9610fe4274c'
        auth_token = '315e2c6da5bc61d837db085c5e04f96c'
        client = Client(account_sid, auth_token)

        if self.type == 'sms' and len(self.content) <= 160:
            message = client.messages.create(
                body=self.content,
                from_=f'{self.sender.telephone}',
                to=f'+{self.recipient.telephone}'
            )
            print(message)

        elif self.type == 'call':
            message = client.messages.create(
                url=self.url_twilio_demo,
                from_=f'{self.sender.telephone}',
                to=f'+{self.recipient.telephone}'
            )
            print(message)

        super().save(*args, **kwargs)"""


class SmsMessages(models.Model):
    recipient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    sender = models.ForeignKey(Psy, on_delete=models.CASCADE)
    corps = models.TextField(max_length=160)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.corps

    def save(self, *args, **kwargs):
        if len(self.corps) < 160:
            account_sid = 'AC3330ae3a0049673de9c3e9610fe4274c'
            auth_token = '315e2c6da5bc61d837db085c5e04f96c'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body=f"{self.corps}",
                from_=f'{self.sender.telephone}',
                to=f'+{self.recipient.telephone}'
            )
            print(message)
        else:
            return None

        super().save()


class AppelClientTwilio(models.Model):
    url_twilio_demo = models.URLField()
    calling_from = models.ForeignKey(Psy, on_delete=models.CASCADE)
    calling_receive = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        account_sid = 'AC3330ae3a0049673de9c3e9610fe4274c'
        auth_token = '315e2c6da5bc61d837db085c5e04f96c'
        client = Client(account_sid, auth_token)
        message = (client.messages.create
            (
            url=f"{self.url_twilio_demo}",
            from_=f'{self.calling_from.user.telephone}',
            to=f'+{self.calling_receive.patient.telephone}'
        )
        )
        print(message)
        super().save()


class VideoCall(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='video_calls_as_patient')
    psy = models.ForeignKey(Psy, on_delete=models.CASCADE, related_name='video_calls_as_psy')
    room_sid = models.CharField(max_length=34, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,
                              choices=[('pending', 'Pending'), ('ongoing', 'Ongoing'), ('finished', 'Finished')],
                              default='pending')

    def __str__(self):
        return f"{self.psy.user.username} <-> {self.patient.user.username}"


class EmailConsultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    psy = models.ForeignKey(Psy, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    received_at = models.DateTimeField(null=True, blank=True)

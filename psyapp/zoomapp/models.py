from django.db import models
from twilio.rest import Client

from accounts.models import Patient, Psy


# Create your models here.


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

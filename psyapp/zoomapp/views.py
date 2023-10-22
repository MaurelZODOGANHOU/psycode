from rest_framework import generics, permissions
from .models import SmsMessages, AppelClientTwilio
from .serializers import SmsMessagesSerializer, AppelClientTwilioSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from twilio.rest import Client
from twilio.twiml.voice_response import Dial, VoiceResponse

from accounts.models import Psy, Patient
from .serializers import CommunicationSerializer


class SmsMessagesListCreateView(generics.ListCreateAPIView):
    queryset = SmsMessages.objects.all()
    serializer_class = SmsMessagesSerializer
    permission_classes = [permissions.IsAuthenticated]  # Autoriser seulement les utilisateurs authentifiés


class SmsMessagesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SmsMessages.objects.all()
    serializer_class = SmsMessagesSerializer
    permission_classes = [permissions.IsAuthenticated]  # Autoriser seulement les utilisateurs authentifiés


class AppelClientTwilioListCreateView(generics.ListCreateAPIView):
    queryset = AppelClientTwilio.objects.all()
    serializer_class = AppelClientTwilioSerializer
    permission_classes = [permissions.IsAuthenticated]  # Autoriser seulement les utilisateurs authentifiés


class AppelClientTwilioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AppelClientTwilio.objects.all()
    serializer_class = AppelClientTwilioSerializer
    permission_classes = [permissions.IsAuthenticated]  # Autoriser seulement les utilisateurs authentifiés


from rest_framework.views import APIView


class CommunicationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CommunicationSerializer(data=request.data)
        if serializer.is_valid():
            sender_id = serializer.validated_data.get('sender_id')
            recipient_id = serializer.validated_data.get('recipient_id')

            sender = get_object_or_404(Psy, pk=sender_id)
            recipient = get_object_or_404(Patient, pk=recipient_id)

            # Votre logique pour mettre en communication ici
            account_sid = 'AC3330ae3a0049673de9c3e9610fe4274c'
            auth_token = '315e2c6da5bc61d837db085c5e04f96c'
            client = Client(account_sid, auth_token)

            # Exemple d'envoi d'un SMS pour initier la communication
            message = client.messages.create(
                body="Votre session de communication va commencer.",
                from_=sender.telephone,
                to=recipient.telephone
            )
            print(message.sid)

            return Response({"detail": "Communication initiée avec succès."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AudioCallView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CommunicationSerializer(data=request.data)
        if serializer.is_valid():
            sender_id = serializer.validated_data.get('sender_id')
            recipient_id = serializer.validated_data.get('recipient_id')

            sender = get_object_or_404(Psy, pk=sender_id)
            recipient = get_object_or_404(Patient, pk=recipient_id)

            # Votre logique pour initier l'appel ici
            account_sid = 'AC3330ae3a0049673de9c3e9610fe4274c'
            auth_token = '315e2c6da5bc61d837db085c5e04f96c'
            client = Client(account_sid, auth_token)

            # Création de la réponse TwiML pour initier l'appel
            response = VoiceResponse()
            response.say("Connexion à votre interlocuteur, veuillez patienter.", voice='alice')
            response.dial(recipient.telephone, callerId=sender.telephone)

            # Initiation de l'appel
            call = client.calls.create(
                to=recipient.telephone,
                from_=sender.telephone,
                twiml=str(response)
            )
            print(call.sid)

            return Response({"detail": "Appel initié avec succès."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

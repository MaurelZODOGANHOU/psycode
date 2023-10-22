from rest_framework import generics, permissions
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

from .models import SmsMessages, AppelClientTwilio
from .serializers import SmsMessagesSerializer, AppelClientTwilioSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from twilio.twiml.voice_response import Dial, VoiceResponse
from twilio.rest import Client
from django.conf import settings
from rest_framework import generics
from .models import VideoCall
from .serializers import VideoCallSerializer
from rest_framework.permissions import IsAuthenticated
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


class VideoCallListCreateView(generics.ListCreateAPIView):
    queryset = VideoCall.objects.all()
    serializer_class = VideoCallSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Créer une salle Twilio et obtenir le SID
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        room = client.video.rooms.create(unique_name=str(uuid.uuid4()), type='group')

        # Mettre à jour le statut et le SID de la salle dans l'instance
        serializer.save(status='pending', room_sid=room.sid)


class VideoCallDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VideoCall.objects.all()
    serializer_class = VideoCallSerializer
    permission_classes = [IsAuthenticated]


class GenerateVideoToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        room_sid = request.data.get('room_sid')
        try:
            video_call = VideoCall.objects.get(room_sid=room_sid)
        except VideoCall.DoesNotExist:
            return Response({'error': 'Video call does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Vérifiez si l'utilisateur est autorisé à rejoindre cet appel vidéo
        if request.user != video_call.patient.user and request.user != video_call.psy.user:
            return Response({'error': 'You are not part of this video call'}, status=status.HTTP_403_FORBIDDEN)

        # Créer le jeton d'accès Twilio
        token = AccessToken(settings.TWILIO_ACCOUNT_SID,
                            settings.TWILIO_API_KEY_SID,
                            settings.TWILIO_API_KEY_SECRET,
                            identity=str(request.user.id))
        video_grant = VideoGrant(room=video_call.room_sid)
        token.add_grant(video_grant)

        return Response({'token': token.to_jwt().decode()})

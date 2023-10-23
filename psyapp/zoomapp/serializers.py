from .models import SmsMessages
from .models import AppelClientTwilio
from .models import VideoCall
from rest_framework import serializers
from .models import EmailConsultation


class EmailConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailConsultation
        fields = '__all__'  # ou une liste des champs que vous voulez inclure


class SmsMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmsMessages
        fields = '__all__'


class CommunicationSerializer(serializers.Serializer):
    sender_id = serializers.IntegerField()
    recipient_id = serializers.IntegerField()


class VideoCallSerializer(serializers.ModelSerializer):
    patient_username = serializers.ReadOnlyField(source='patient.user.username')
    psy_username = serializers.ReadOnlyField(source='psy.user.username')

    class Meta:
        model = VideoCall
        fields = ['id', 'patient', 'psy', 'room_sid', 'created_at', 'status', 'patient_username', 'psy_username']
        read_only_fields = ['room_sid', 'created_at', 'status', 'patient_username', 'psy_username']


class AppelClientTwilioSerializer(serializers.ModelSerializer):
    calling_from_username = serializers.ReadOnlyField(source='calling_from.user.username')
    calling_receive_username = serializers.ReadOnlyField(source='calling_receive.user.username')

    class Meta:
        model = AppelClientTwilio
        fields = ['id', 'url_twilio_demo', 'calling_from', 'calling_receive', 'calling_from_username',
                  'calling_receive_username']
        read_only_fields = ['calling_from_username', 'calling_receive_username']

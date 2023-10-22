from rest_framework import serializers
from .models import SmsMessages, AppelClientTwilio


class SmsMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmsMessages
        fields = '__all__'


class AppelClientTwilioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppelClientTwilio
        fields = '__all__'


from rest_framework import serializers


class CommunicationSerializer(serializers.Serializer):
    sender_id = serializers.IntegerField()
    recipient_id = serializers.IntegerField()


from rest_framework import serializers
from .models import VideoCall


class VideoCallSerializer(serializers.ModelSerializer):
    patient_username = serializers.ReadOnlyField(source='patient.user.username')
    psy_username = serializers.ReadOnlyField(source='psy.user.username')

    class Meta:
        model = VideoCall
        fields = ['id', 'patient', 'psy', 'room_sid', 'created_at', 'status', 'patient_username', 'psy_username']
        read_only_fields = ['room_sid', 'created_at', 'status', 'patient_username', 'psy_username']

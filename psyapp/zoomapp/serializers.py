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

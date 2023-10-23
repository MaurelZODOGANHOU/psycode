from rest_framework import serializers
from .models import SpecialisationPsy, ForfaitConsultation, SouscriptionForfait, Consultation, Commande


class SpecialisationPsySerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialisationPsy
        fields = '__all__'


class ForfaitConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForfaitConsultation
        fields = '__all__'


class SouscriptionForfaitSerializer(serializers.ModelSerializer):
    forfait = ForfaitConsultationSerializer(read_only=True)

    class Meta:
        model = SouscriptionForfait
        fields = '__all__'


class ConsultationSerializer(serializers.ModelSerializer):
    souscription = SouscriptionForfaitSerializer(read_only=True)

    class Meta:
        model = Consultation
        fields = '__all__'


class CommandeSerializer(serializers.ModelSerializer):
    consultation = ConsultationSerializer(read_only=True)

    class Meta:
        model = Commande
        fields = '__all__'

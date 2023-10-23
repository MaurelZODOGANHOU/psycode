from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import SpecialisationPsy, ForfaitConsultation, SouscriptionForfait, Consultation, Commande
from .serializers import SpecialisationPsySerializer, ForfaitConsultationSerializer, SouscriptionForfaitSerializer, \
    ConsultationSerializer, CommandeSerializer


class SpecialisationPsyListCreateView(generics.ListCreateAPIView):
    queryset = SpecialisationPsy.objects.all()
    serializer_class = SpecialisationPsySerializer
    permission_classes = [permissions.IsAuthenticated]


class SpecialisationPsyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SpecialisationPsy.objects.all()
    serializer_class = SpecialisationPsySerializer
    permission_classes = [permissions.IsAuthenticated]


class ForfaitConsultationListCreateView(generics.ListCreateAPIView):
    queryset = ForfaitConsultation.objects.all()
    serializer_class = ForfaitConsultationSerializer
    permission_classes = [permissions.IsAuthenticated]


class ForfaitConsultationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ForfaitConsultation.objects.all()
    serializer_class = ForfaitConsultationSerializer
    permission_classes = [permissions.IsAuthenticated]


class SouscriptionForfaitListCreateView(generics.ListCreateAPIView):
    queryset = SouscriptionForfait.objects.all()
    serializer_class = SouscriptionForfaitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)


class SouscriptionForfaitDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SouscriptionForfait.objects.all()
    serializer_class = SouscriptionForfaitSerializer
    permission_classes = [permissions.IsAuthenticated]


class ConsultationListCreateView(generics.ListCreateAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        ConsultationService.create_consultation(serializer, self.request.user)


class ConsultationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommandeListCreateView(generics.ListCreateAPIView):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        PaymentService.create_payment_intent(serializer, self.request.user)


class CommandeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer
    permission_classes = [permissions.IsAuthenticated]

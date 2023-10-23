from rest_framework import generics
from .models import Specialisation, Panier
from .serializers import SpecialisationSerializer, PanierSerializer


class SpecialisationList(generics.ListCreateAPIView):
    queryset = Specialisation.objects.all()
    serializer_class = SpecialisationSerializer


class SpecialisationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Specialisation.objects.all()
    serializer_class = SpecialisationSerializer


class PanierList(generics.ListCreateAPIView):
    queryset = Panier.objects.all()
    serializer_class = PanierSerializer


class PanierDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Panier.objects.all()
    serializer_class = PanierSerializer

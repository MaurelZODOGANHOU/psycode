# views.py
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User
from .serializers import UserRegisterSerializer

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Psy, LieuConsultation, Cabinet, Patient
from .serializers import PsySerializer, LieuConsultationSerializer, CabinetSerializer, PatientSerializer


# Pour Psy
class PsyListCreateView(generics.ListCreateAPIView):
    queryset = Psy.objects.all()
    serializer_class = PsySerializer
    permission_classes = [IsAuthenticated]


class PsyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Psy.objects.all()
    serializer_class = PsySerializer
    permission_classes = [IsAuthenticated]


# Pour LieuConsultation
class LieuConsultationListCreateView(generics.ListCreateAPIView):
    queryset = LieuConsultation.objects.all()
    serializer_class = LieuConsultationSerializer
    permission_classes = [IsAuthenticated]


class LieuConsultationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LieuConsultation.objects.all()
    serializer_class = LieuConsultationSerializer
    permission_classes = [IsAuthenticated]


# Pour Cabinet
class CabinetListCreateView(generics.ListCreateAPIView):
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer
    permission_classes = [IsAuthenticated]


class CabinetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer
    permission_classes = [IsAuthenticated]


# Pour Patient
class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]


class PatientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            if user.user_type == 'Psy':
                return Response({"user_id": user.id, "profile_type": "Psy"}, status=status.HTTP_201_CREATED)
            elif user.user_type == 'Patient':
                return Response({"user_id": user.id, "profile_type": "Patient"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

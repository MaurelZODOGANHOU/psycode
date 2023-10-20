# views.py
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User
from .serializers import UserRegisterSerializer


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

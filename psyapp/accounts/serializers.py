# serializers.py
from rest_framework import serializers
from .models import User, Psy, Patient


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'nom', 'prenom', 'middle_name', 'username', 'date_naissance', 'telephone',
                  'user_type']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user_type = validated_data.get('user_type')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        if user_type == "Psy":
            Psy.objects.create(user=user)
        elif user_type == "Patient":
            Patient.objects.create(user=user, pseudo=validated_data.get('pseudo'))

        return user

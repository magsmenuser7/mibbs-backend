# accounts/serializers.py
from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'password']

    def create(self, validated_data):
        # Optionally, you can hash the password here using make_password
        return UserProfile.objects.create(**validated_data)




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
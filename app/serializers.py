from rest_framework import serializers
from .models import Users, Role, UserRole
from rest_framework import serializers

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source='role', write_only=True, required=False
    )

    class Meta:
        model = Users
        exclude = ('password',)  # ✅ Removed 'history'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('username', 'email', 'phone', 'password')

    def validate(self, data):
        if Users.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})
        if Users.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'Username already exists'})
        if Users.objects.filter(phone=data['phone']).exists():
            raise serializers.ValidationError({'phone': 'Phone number already exists'})
        return data

    def create(self, validated_data):
        user = Users.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            password=validated_data['password']
        )
        return user
    


class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()  # this can be email or phone
    password = serializers.CharField(write_only=True)









# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     phone = serializers.CharField(required=False, allow_blank=True)
#     password = serializers.CharField(write_only=True)












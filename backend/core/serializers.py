from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = (
            'username', 
            'password', 
            'email',
            'age',
            'location',
            'personality_type',
            'personality_details',
            'available_time',
            'budget_preference'
        )
        extra_kwargs = {
            'personality_type': {'required': False},
            'personality_details': {'required': False},
            'available_time': {'required': False},
            'budget_preference': {'required': False},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # Set profile_completed to False by default
        user.profile_completed = False
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'age', 'location', 'personality_type', 
                 'available_time', 'budget_preference', 'profile_completed', 
                 'coins', 'exp')
        read_only_fields = ('coins', 'exp')
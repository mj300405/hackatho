from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from core.utils import get_incomplete_fields

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
        # Create the user
        user = User.objects.create_user(**validated_data)
        
        # Check if profile is complete
        incomplete_fields = get_incomplete_fields(user)
        user.profile_completed = not bool(incomplete_fields)
        
        # Save the user with updated profile_completed status
        user.save()
        
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'age', 'location', 'personality_type', 
                 'available_time', 'budget_preference', 'profile_completed', 
                 'coins', 'exp')
        read_only_fields = ('coins', 'exp', 'profile_completed')

    def update(self, instance, validated_data):
        # Update the user instance with validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Check if profile is complete after update
        incomplete_fields = get_incomplete_fields(instance)
        instance.profile_completed = not bool(incomplete_fields)
        
        instance.save()
        return instance
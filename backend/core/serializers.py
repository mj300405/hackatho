from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Hobby, Category

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

class HobbyRecommendationSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(write_only=True)
    match_level = serializers.CharField(write_only=True)
    
    class Meta:
        model = Hobby
        fields = (
            'id',
            'name', 
            'description', 
            'difficulty_level', 
            'time_commitment',
            'price_range', 
            'required_equipment', 
            'minimum_age', 
            'category_name',
            'match_level'
        )

    def create(self, validated_data):
        category_name = validated_data.pop('category_name')
        validated_data.pop('match_level', None)  # Remove match_level as it's not part of the Hobby model
        category, _ = Category.objects.get_or_create(name=category_name)
        return Hobby.objects.create(category=category, **validated_data)
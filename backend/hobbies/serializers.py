from rest_framework import serializers
from .models import Hobby, Category, UserHobby, HobbyTasting

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')

class HobbySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Hobby
        fields = (
            'id',
            'name', 
            'description', 
            'category',
            'difficulty_level', 
            'time_commitment',
            'price_range', 
            'required_equipment', 
            'minimum_age'
        )

class UserHobbySerializer(serializers.ModelSerializer):
    hobby = HobbySerializer(read_only=True)
    
    class Meta:
        model = UserHobby
        fields = (
            'id',
            'hobby',
            'status',
            'notes',
            'resources_links',
            'started_at',
            'last_activity',
            'rating'
        )
from rest_framework import serializers
from hobbies.models import Hobby, Category
from .models import RouletteHistory

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
        validated_data.pop('match_level', None)
        category, _ = Category.objects.get_or_create(name=category_name)
        return Hobby.objects.create(category=category, **validated_data)

class RouletteHistorySerializer(serializers.ModelSerializer):
    hobby = HobbyRecommendationSerializer(read_only=True)
    
    class Meta:
        model = RouletteHistory
        fields = ('id', 'hobby', 'suggested_at', 'was_accepted', 'coins_spent')
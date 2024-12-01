from rest_framework import serializers
from .models import Hobby, Category, UserHobby, Tag

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')

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

class HobbyDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    is_active = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField()
    user_notes = serializers.SerializerMethodField()
    
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
            'minimum_age',
            'notes',
            'tags',
            'is_active',
            'is_favorite',
            'user_rating',
            'user_notes',
            'created_at'
        )
    
    def get_is_active(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserHobby.objects.filter(
                user=request.user,
                hobby=obj,
                status='active'
            ).exists()
        return False
    
    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserHobby.objects.filter(
                user=request.user,
                hobby=obj,
                status='favorite'
            ).exists()
        return False
    
    def get_user_rating(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user_hobby = UserHobby.objects.filter(
                user=request.user,
                hobby=obj
            ).first()
            return user_hobby.rating if user_hobby else None
        return None
    
    def get_user_notes(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user_hobby = UserHobby.objects.filter(
                user=request.user,
                hobby=obj
            ).first()
            return user_hobby.notes if user_hobby else None
        return None
from rest_framework import serializers
from .models import Challenge
from hobbies.serializers import HobbySerializer

class ChallengeSerializer(serializers.ModelSerializer):
    hobby = HobbySerializer(read_only=True)
    
    class Meta:
        model = Challenge
        fields = (
            'id',
            'hobby',
            'description',
            'reward',
            'progress',
            'target',
            'successful',
            'expiration_date'
        )
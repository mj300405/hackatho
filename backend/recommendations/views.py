from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.shortcuts import get_object_or_404
from core.decorators import profile_completed_required
from .services import HobbyRecommendationService
from hobbies.models import Hobby, Category, UserHobby
from .serializers import HobbyRecommendationSerializer
from core.models import User

class InitialHobbyRecommendationView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HobbyRecommendationSerializer
    
    def get(self, request, user_id):
        """
        Get existing initial recommendations for a user
        """
        # Verify user access
        if request.user.id != user_id:
            return Response({
                "error": "Permission denied",
                "message": "You can only view recommendations for your own account."
            }, status=status.HTTP_403_FORBIDDEN)
            
        target_user = get_object_or_404(User, id=user_id)
        
        # Get existing recommendations
        user_hobbies = UserHobby.objects.filter(user=target_user)
        if not user_hobbies.exists():
            return Response({
                "message": "No recommendations found. Please generate initial recommendations first.",
                "recommendations": []
            }, status=status.HTTP_200_OK)
            
        # Prepare response data
        response_data = []
        for user_hobby in user_hobbies:
            hobby_dict = self.serializer_class(user_hobby.hobby).data
            hobby_dict['status'] = user_hobby.status
            response_data.append(hobby_dict)
            
        return Response({
            "message": "Retrieved existing recommendations",
            "recommendations": response_data
        })

    @profile_completed_required()
    def post(self, request, user_id):
        """
        Generate initial recommendations for a user
        """
        # Verify user access
        if request.user.id != user_id:
            return Response({
                "error": "Permission denied",
                "message": "You can only generate recommendations for your own account."
            }, status=status.HTTP_403_FORBIDDEN)
            
        target_user = get_object_or_404(User, id=user_id)
        
        # Check if user already has recommendations
        if target_user.user_hobbies.exists():
            return Response({
                "error": "Initial recommendations already generated",
                "message": "You already have hobby recommendations. Use the hobby roulette for more suggestions."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify user profile is complete
        if not target_user.profile_completed:
            return Response({
                "error": "Profile incomplete",
                "message": "Please complete your profile before generating recommendations."
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            # Generate recommendations
            service = HobbyRecommendationService()
            recommendations = service.get_recommendations(target_user)
            
            if not recommendations:
                return Response({
                    "error": "Failed to generate recommendations",
                    "message": "Please try again later."
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            with transaction.atomic():
                created_hobbies = []
                
                for recommendation in recommendations:
                    # Create or get hobby
                    hobby, created = Hobby.objects.get_or_create(
                        name__iexact=recommendation['name'],
                        defaults={
                            'name': recommendation['name'],
                            'description': recommendation['description'],
                            'difficulty_level': recommendation['difficulty_level'],
                            'time_commitment': recommendation['time_commitment'],
                            'price_range': recommendation['price_range'],
                            'required_equipment': recommendation['required_equipment'],
                            'minimum_age': recommendation['minimum_age']
                        }
                    )
                    
                    # Create or get category
                    category, _ = Category.objects.get_or_create(
                        name=recommendation['category_name']
                    )
                    hobby.category = category
                    hobby.save()
                    
                    created_hobbies.append({
                        'hobby': hobby,
                        'match_level': recommendation['match_level'],
                        'location_suitable': recommendation.get('location_suitable', True),
                        'personality_match': recommendation.get('personality_match', '')
                    })
                
                # Create UserHobby entries
                for hobby_data in created_hobbies:
                    UserHobby.objects.create(
                        user=target_user,
                        hobby=hobby_data['hobby'],
                        status='favorite' if hobby_data['match_level'] == 'BEST' else 'active'
                    )
                
                # Prepare response data
                response_data = []
                for hobby_data in created_hobbies:
                    hobby_dict = self.serializer_class(hobby_data['hobby']).data
                    hobby_dict.update({
                        'match_level': hobby_data['match_level'],
                        'location_suitable': hobby_data['location_suitable'],
                        'personality_match': hobby_data['personality_match']
                    })
                    response_data.append(hobby_dict)
                
                return Response({
                    "message": "Initial recommendations generated successfully",
                    "recommendations": response_data
                })
                
        except Exception as e:
            return Response({
                "error": "Error processing recommendations",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
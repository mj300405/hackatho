from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from core.decorators import profile_completed_required
from .services import HobbyRecommendationService
from hobbies.models import Hobby, Category, UserHobby
from .serializers import HobbyRecommendationSerializer

class InitialHobbyRecommendationView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HobbyRecommendationSerializer
    
    @profile_completed_required()
    def get(self, request):
        # Check if user already has recommendations
        if request.user.user_hobbies.exists():
            return Response({
                "error": "Initial recommendations already generated",
                "message": "You already have hobby recommendations. Use the hobby roulette for more suggestions."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        service = HobbyRecommendationService()
        recommendations = service.get_recommendations(request.user)
        
        if not recommendations:
            return Response({
                "error": "Failed to generate recommendations",
                "message": "Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            with transaction.atomic():
                created_hobbies = []
                
                for recommendation in recommendations:
                    # Check if hobby already exists
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
                    
                    category, _ = Category.objects.get_or_create(
                        name=recommendation['category_name']
                    )
                    hobby.category = category
                    hobby.save()
                    
                    created_hobbies.append({
                        'hobby': hobby,
                        'match_level': recommendation['match_level']
                    })
                
                # Create UserHobby entries
                for hobby_data in created_hobbies:
                    UserHobby.objects.create(
                        user=request.user,
                        hobby=hobby_data['hobby'],
                        status='favorite' if hobby_data['match_level'] == 'BEST' else 'active'
                    )
                
                # Prepare response data
                response_data = []
                for hobby_data in created_hobbies:
                    hobby_dict = self.serializer_class(hobby_data['hobby']).data
                    hobby_dict['match_level'] = hobby_data['match_level']
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
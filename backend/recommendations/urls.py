# recommendations/urls.py
from django.urls import path
from .views import InitialHobbyRecommendationView

urlpatterns = [
    path('initial/<int:user_id>/', InitialHobbyRecommendationView.as_view(), name='initial_recommendations'),
]
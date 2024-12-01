# recommendations/urls.py
from django.urls import path
from .views import InitialHobbyRecommendationView, ExploreRecommendationsView, RouletteView

urlpatterns = [
    path('initial/<int:user_id>/', InitialHobbyRecommendationView.as_view(), name='initial_recommendations'),
    path('explore/', ExploreRecommendationsView.as_view(), name='explore_recommendations'),
    path('roulette/', RouletteView.as_view(), name='hobby_roulette'),
]
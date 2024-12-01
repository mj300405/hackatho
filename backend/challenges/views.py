from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction

from .models import Challenge
from .serializers import ChallengeSerializer
from .services import ChallengeGenerationService
from hobbies.models import Hobby
from core.decorators import profile_completed_required

class ChallengeViewSet(viewsets.ModelViewSet):
    serializer_class = ChallengeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return challenges for the current user"""
        return Challenge.objects.filter(user=self.request.user)

    @profile_completed_required()
    def create(self, request, *args, **kwargs):
        """Generate a new challenge for a specific hobby"""
        hobby_id = request.data.get('hobby_id')
        if not hobby_id:
            return Response(
                {"error": "hobby_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        hobby = get_object_or_404(Hobby, id=hobby_id)

        # Check if user has any active challenges for this hobby
        active_challenge = Challenge.objects.filter(
            user=request.user,
            hobby=hobby,
            successful=False,
            expiration_date__gt=timezone.now()
        ).first()

        if active_challenge:
            return Response({
                "error": "Active challenge exists",
                "message": "Complete or wait for your current challenge to expire",
                "challenge": ChallengeSerializer(active_challenge).data
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get past challenges for this hobby
        past_challenges = Challenge.objects.filter(
            user=request.user,
            hobby=hobby
        ).order_by('-created_at')[:5]

        try:
            service = ChallengeGenerationService()
            challenge = service.generate_challenge(
                user=request.user,
                hobby=hobby,
                past_challenges=past_challenges
            )

            # Save the challenge
            challenge.save()

            return Response(
                ChallengeSerializer(challenge).data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response({
                "error": "Failed to generate challenge",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        """Update the progress of a challenge"""
        challenge = self.get_object()

        # Verify challenge is still active
        if challenge.expiration_date < timezone.now():
            return Response({
                "error": "Challenge expired",
                "message": "This challenge has expired"
            }, status=status.HTTP_400_BAD_REQUEST)

        if challenge.successful:
            return Response({
                "error": "Challenge completed",
                "message": "This challenge is already completed"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get progress increment from request
        increment = request.data.get('increment', 1)
        try:
            increment = int(increment)
            if increment <= 0:
                raise ValueError("Increment must be positive")
        except (TypeError, ValueError):
            return Response({
                "error": "Invalid increment",
                "message": "Increment must be a positive integer"
            }, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Update progress
            challenge.progress = min(challenge.progress + increment, challenge.target)
            
            # Check if challenge is completed
            if challenge.progress >= challenge.target:
                challenge.successful = True
                challenge.progress = challenge.target
                
                # Award coins to user
                request.user.coins += challenge.reward
                request.user.save()

            challenge.save()

        return Response(ChallengeSerializer(challenge).data)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active challenges for the user"""
        active_challenges = Challenge.objects.filter(
            user=request.user,
            successful=False,
            expiration_date__gt=timezone.now()
        )
        return Response(ChallengeSerializer(active_challenges, many=True).data)

    @action(detail=False, methods=['get'])
    def completed(self, request):
        """Get all completed challenges for the user"""
        completed_challenges = Challenge.objects.filter(
            user=request.user,
            successful=True
        ).order_by('-created_at')
        return Response(ChallengeSerializer(completed_challenges, many=True).data)

    @action(detail=False, methods=['get'])
    def expired(self, request):
        """Get all expired and uncompleted challenges for the user"""
        expired_challenges = Challenge.objects.filter(
            user=request.user,
            successful=False,
            expiration_date__lt=timezone.now()
        ).order_by('-expiration_date')
        return Response(ChallengeSerializer(expired_challenges, many=True).data)

    def destroy(self, request, *args, **kwargs):
        """Prevent challenge deletion"""
        return Response({
            "error": "Operation not allowed",
            "message": "Challenges cannot be deleted"
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
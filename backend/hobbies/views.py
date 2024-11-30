from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import UserHobby
from .serializers import UserHobbySerializer
from core.decorators import profile_completed_required

class UserHobbyListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserHobbySerializer

    def get_queryset(self):
        return UserHobby.objects.filter(user=self.request.user)

class UserHobbyDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserHobbySerializer
    lookup_field = 'hobby_id'

    def get_queryset(self):
        return UserHobby.objects.filter(user=self.request.user)

class UpdateHobbyStatusView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserHobbySerializer

    def get_object(self):
        return UserHobby.objects.get(
            user=self.request.user,
            hobby_id=self.kwargs['hobby_id']
        )

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except UserHobby.DoesNotExist:
            return Response(
                {"error": "Hobby not found for this user"},
                status=status.HTTP_404_NOT_FOUND
            )
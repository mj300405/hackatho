from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import UserHobby
from .serializers import UserHobbySerializer

class UserHobbyListView(generics.ListAPIView):
    """
    Get list of all user's hobbies.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserHobbySerializer

    def get_queryset(self):
        return UserHobby.objects.filter(user=self.request.user)

class UserHobbyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, update or delete specific user hobby.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserHobbySerializer
    lookup_field = 'hobby_id'

    def get_queryset(self):
        return UserHobby.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserHobby.DoesNotExist:
            return Response(
                {"error": "Hobby not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class UpdateHobbyStatusView(generics.UpdateAPIView):
    """
    Update hobby status (active/favorite/completed).
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserHobbySerializer

    def get_object(self):
        try:
            return UserHobby.objects.get(
                user=self.request.user,
                hobby_id=self.kwargs['hobby_id']
            )
        except UserHobby.DoesNotExist:
            return None

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response(
                {"error": "Hobby not found for this user"},
                status=status.HTTP_404_NOT_FOUND
            )

        if 'status' not in request.data:
            return Response(
                {"error": "Status field is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.data['status'] not in ['active', 'favorite', 'completed']:
            return Response(
                {"error": "Invalid status. Must be one of: active, favorite, completed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
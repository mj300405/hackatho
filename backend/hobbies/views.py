from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import UserHobby, Hobby
from .serializers import UserHobbySerializer, HobbyDetailSerializer, UserHobbyListSerializer
from django.db import transaction
from django.db.models import Q

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

class BulkUpdateHobbyStatusView(generics.UpdateAPIView):
    """
    Update status for multiple hobbies at once.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserHobbySerializer

    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            return Response(
                {"error": "Request data must be a list of hobby status updates"},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = []
        errors = []

        for item in request.data:
            if not isinstance(item, dict) or 'hobby_id' not in item or 'status' not in item:
                errors.append({
                    "error": "Each item must contain hobby_id and status",
                    "item": item
                })
                continue

            if item['status'] not in ['active', 'favorite', 'completed']:
                errors.append({
                    "error": "Invalid status. Must be one of: active, favorite, completed",
                    "item": item
                })
                continue

            try:
                hobby = UserHobby.objects.get(
                    user=request.user,
                    hobby_id=item['hobby_id']
                )
                serializer = self.get_serializer(hobby, data={'status': item['status']}, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    results.append(serializer.data)
                else:
                    errors.append({
                        "error": "Validation failed",
                        "hobby_id": item['hobby_id'],
                        "details": serializer.errors
                    })
            except UserHobby.DoesNotExist:
                errors.append({
                    "error": "Hobby not found",
                    "hobby_id": item['hobby_id']
                })

        response_data = {
            "updated": results,
            "errors": errors if errors else None
        }

        # If there were only errors and no successful updates, return 400
        if not results and errors:
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        return Response(response_data, status=status.HTTP_200_OK)

class HobbyDetailView(generics.RetrieveAPIView):
    queryset = Hobby.objects.all()
    serializer_class = HobbyDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class UserHobbiesView(generics.ListAPIView):
    """
    Get list of user's hobbies with optional status filtering.
    
    Query Parameters:
    - status: Filter by status (active/favorite/completed)
    - search: Search hobbies by name
    - sort: Sort by field (name, started_at, last_activity)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserHobbyListSerializer

    def get_queryset(self):
        queryset = UserHobby.objects.filter(user=self.request.user)\
            .select_related('hobby', 'hobby__category')\
            .prefetch_related('hobby__tags')
        
        # Status filtering
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
            
        # Search by hobby name
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(hobby__name__icontains=search) | 
                Q(hobby__description__icontains=search)
            )
            
        # Sorting
        sort_by = self.request.query_params.get('sort', 'started_at')
        sort_mapping = {
            'name': 'hobby__name',
            'started_at': '-started_at',
            'last_activity': '-last_activity'
        }
        queryset = queryset.order_by(sort_mapping.get(sort_by, '-started_at'))
        
        return queryset
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # Group hobbies by status
        hobbies_by_status = {
            'active': [],
            'favorite': [],
            'completed': []
        }
        
        for hobby in serializer.data:
            status = hobby['status']
            hobbies_by_status[status].append(hobby)
            
        return Response({
            'total_count': queryset.count(),
            'hobbies': hobbies_by_status
        })

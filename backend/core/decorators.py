from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from core.utils import get_incomplete_fields

def profile_completed_required():
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view_instance, request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise AuthenticationFailed("Authentication required")
            
            if not request.user.profile_completed:
                return Response(
                    {
                        "error": "Profile incomplete",
                        "message": "Please complete your profile before accessing this feature",
                        "required_fields": get_incomplete_fields(request.user)
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            return view_func(view_instance, request, *args, **kwargs)
        return _wrapped_view
    return decorator

def check_roulette_access():
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view_instance, request, *args, **kwargs):
            if not request.user.can_use_roulette_free():
                coins_needed = request.user.get_roulette_cost()
                if request.user.coins < coins_needed:
                    return Response(
                        {
                            "error": "Insufficient coins",
                            "coins_needed": coins_needed,
                            "current_coins": request.user.coins,
                            "next_free_spin": request.user.get_next_free_roulette_time()
                        },
                        status=status.HTTP_403_FORBIDDEN
                    )
            return view_func(view_instance, request, *args, **kwargs)
        return _wrapped_view
    return decorator
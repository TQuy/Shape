from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from authentication.models import User
import jwt

def token_required(f):
    """
    required authentication to access
    """
    @wraps(f)
    def decorator(request, *args, **kwargs):
        token = None
        print(request.headers)
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        
        if not token:
            return Response({
                "error": "token required!"
            }, status=status.HTTP_401_UNAUTHORIZED)

        try:
            data = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]                
            )

        except BaseException:
            return Response({
                "error": "invalid token!"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            current_user = User.objects.filter(id=data['id']).first()
            if current_user is None:
                return Response({
                    "error": "incorrect username or password!"
                }, status=status.HTTP_400_BAD_REQUEST)
            request.user = current_user

        except:
            return Response({
                "error": "Unexpected error!"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return f(request, *args, **kwargs)

    return decorator

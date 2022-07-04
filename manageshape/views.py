from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from authentication.models import User
from manageshape.models import Shape
import jwt
from django.conf import settings
from authentication.decorators import token_required

@token_required
@api_view(["GET"])
def shapes(request):
    if request.method == 'GET':
        shapes = request.user.shape_set.values('id', 'name', 'type')
        
        return Response({
            "shapes": shapes
        }, status=status.HTTP_200_OK)

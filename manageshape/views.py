from secrets import choice
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from authentication.models import User
from manageshape.models import Shape
import jwt
from django.conf import settings
from authentication.decorators import token_required
import random

@token_required
@api_view(["GET", "POST"])
def shapes(request, current_user):
    if request.method == "GET":
        print(f"-----------------{current_user.shape_set.all()}")
        shapes = current_user.shape_set.values('id', 'name', 'type')
        
        return Response({
            "shapes": shapes
        }, status=status.HTTP_200_OK)

    # if request.method == "POST":
    #     name = request.data.get("name")

    #     if name is None:
    #         return Response({
    #             "error": "shape name required!"
    #         }, status=status.HTTP_400_BAD_REQUEST)

    #     shape_list = ["triangle", "rectangle", "diamond", "square"]

    #     shape, created = request.user.shape_set.update_or_create(name=name, type=random.choice(shape_list))

    #     if created:
    #         return Response({
    #             "shapes": shape
    #         }, status=status.HTTP_201_CREATED)

    #     return Response({
    #         "shapes": shape
    #     }, status=status.HTTP_200_OK)

@token_required
@api_view(["POST"])
def update_or_create_shape(request, current_user):
    name = request.data.get("name")
    type = request.data.get("type")

    if name is None or type is None:
        return Response({
            "error": "shape name and type are required!"
        }, status=status.HTTP_400_BAD_REQUEST)

    shape = current_user.shape_set.filter(name=name).first()
    # create shape
    if shape is None:
        shape = Shape.objects.create(
            user=current_user,
            name=name,
            type=type
        )
        return Response({
            "shape": {
                "id": shape.id,
                "name": shape.name,
                "type": shape.type
            }
        }, status=status.HTTP_201_CREATED)
    # update shape
    shape.type = type
    shape.save()

    return Response({
        "shape": {
            "id": shape.id,
            "name": shape.name,
            "type": shape.type
        }
    }, status=status.HTTP_200_OK)

@token_required
@api_view(["GET", "DELETE"])
def shape(request, current_user, id):
    if request.method == "GET":
        shape = current_user.shape_set.filter(pk=id).first()

        if shape is None:
            return Response({
                "error": "shape not found!"
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "shapes": {
                "name": shape.name,
                "type": shape.type
            }
        }, status=status.HTTP_200_OK)

    if request.method == "DELETE":
        shape = current_user.shape_set.filter(pk=id).first()

        if shape is None:
            return Response({
                "error": "shape not found!"
            }, status=status.HTTP_404_NOT_FOUND)

        count, _ = current_user.shape_set.filter(id=id).delete()

        if count == 0:
            return Response({
                "error": "deleted failed!"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "data": "OK"
        }, status=status.HTTP_200_OK)
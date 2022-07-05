from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from manageshape.models import Shape
from django.conf import settings
from authentication.decorators import token_required
from manageshape.serializers import ShapeSerializer
from decimal import *
import math
from manageshape import area_equation
from manageshape import perimeter_equation


@token_required
@api_view(["GET"])
def shapes(request, current_user):
    shapes = current_user.shape_set.all()
    shapes_json = ShapeSerializer(shapes, many=True)

    return Response({
        "shapes": shapes_json.data
    }, status=status.HTTP_200_OK)


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
    shape, created = Shape.objects.update_or_create(
        name=name, user=current_user, defaults={"type": type})

    # create shape
    if created:
        shapes_json = ShapeSerializer(shape)

        return Response({
            "shape": shapes_json.data
        }, status=status.HTTP_201_CREATED)

    # update shape
    shapes_json = ShapeSerializer(shape)

    return Response({
        "shape": shapes_json.data
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

        shapes_json = ShapeSerializer(shape)

        return Response({
            "shapes": shapes_json.data
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


@api_view(["GET"])
def compute_area(request):
    type = request.GET.get('type')
    params = request.GET.get('params')

    if type is None or params is None:
        return Response({
            "error": "Type and Params required!"
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        params = params.split(',')
        params = [Decimal(i.strip()) for i in params]
    except BaseException:
        return Response({
            "error": "invalid params!"
        }, status=status.HTTP_400_BAD_REQUEST)

    if any([i == 0 for i in params]):
        return Response({
            "error": "invalid param value!"
        }, status=status.HTTP_400_BAD_REQUEST)

    if type == 'triangle':
        res, err = area_equation.triangle(*params)

    elif type == 'rectangle':
        res, err = area_equation.rectangle(*params)

    elif type == 'square':
        res, err = area_equation.square(*params)

    elif type == 'diamond':
        res, err = area_equation.diamond(*params)

    else:
        return Response({
            "error": "In correct type!"
        }, status=status.HTTP_400_BAD_REQUEST)

    if err is not None:
        return Response({
            "error": err
        }, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        "data": res
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def compute_perimeter(request):
    type = request.GET.get('type')
    params = request.GET.get('params')

    if type is None or params is None:
        return Response({
            "error": "Type and Params required!"
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        params = params.split(',')
        params = [Decimal(i.strip()) for i in params]
    except BaseException:
        return Response({
            "error": "invalid params!"
        }, status=status.HTTP_400_BAD_REQUEST)

    if any([i == 0 for i in params]):
        return Response({
            "error": "invalid param value!"
        }, status=status.HTTP_400_BAD_REQUEST)

    if type == 'triangle':
        res, err = perimeter_equation.triangle(*params)

    elif type == 'rectangle':
        res, err = perimeter_equation.rectangle(*params)

    elif type == 'square':
        res, err = perimeter_equation.square(*params)

    elif type == 'diamond':
        res, err = perimeter_equation.diamond(*params)

    else:
        return Response({
            "error": "In correct type!"
        }, status=status.HTTP_400_BAD_REQUEST)

    if err is not None:
        return Response({
            "error": "In correct type!"
        }, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        "data": res
    }, status=status.HTTP_200_OK)

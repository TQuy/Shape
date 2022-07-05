from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from manageshape.models import Shape
from django.conf import settings
from authentication.decorators import token_required
from manageshape.serializers import ShapeSerializer


@token_required
@api_view(["GET", "POST"])
def shapes(request, current_user):
    if request.method == "GET":
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
    shape, created = Shape.objects.update_or_create(name=name, user=current_user, defaults={"type": type})

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

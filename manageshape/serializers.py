from manageshape.models import Shape
from rest_framework import serializers


class ShapeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shape
        fields = ["id", "name", "type"]

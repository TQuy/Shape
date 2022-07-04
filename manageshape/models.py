from django.db import models
from authentication.models import User


class DateTimeModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True

# Create your models here.


class Shape(DateTimeModel):
    """
    Model for table shapes
    """
    class ShapeType(models.TextChoices):
        TRIANGLE = 'triangle'
        RECTANGLE = 'rectangle'
        SQUARE = 'square'
        DIAMOND = 'diamond'

    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=20,
        choices=ShapeType.choices,
        default=ShapeType.TRIANGLE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta(DateTimeModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'user'],
                name='unique_shape_name'
            )
        ]

    def __str__(self):
        return f"{self.id}: {self.name}"

from django.test import TestCase
from manageshape.models import Shape
from authentication.tests import UserTestCase
from authentication.models import User
from django.db import IntegrityError, transaction
import re

# Create your tests here.

class ShapeTestCase(TestCase):
    def setUp(self):
        self.name = 'tri1'
        self.type = 'triangle'

    def test_shape_model(self):
        shape_list = ['rectangle', 'triangle', 'square', 'diamond']
        UserTestCase.register_user('quynt', '1')
        user = User.objects.first()
        # check create shape
        for i in range(len(shape_list)):
            triangle = Shape.objects.create(name=shape_list[i], type=shape_list[i], user=user)
        self.assertEqual(Shape.objects.count(), len(shape_list))

        # check unique contraint
        with self.assertRaises(IntegrityError) as err:
            with transaction.atomic():
                Shape.objects.create(name=shape_list[0], type=shape_list[0], user=user)
        self.assertTrue(re.match(r"unique", str(err.exception), re.IGNORECASE))

        # check update_or_create
        new_shape = Shape.objects.get(user=user, name=shape_list[0])
        new_shape.type = shape_list[1]
        new_shape.save()

        # check CASCADE delete
        user.delete()
        self.assertEqual(Shape.objects.count(), 0)
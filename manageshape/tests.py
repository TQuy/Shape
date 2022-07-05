from django.test import TestCase
from manageshape.models import Shape
from authentication.tests import UserTestCase
from authentication.models import User
from django.db import IntegrityError, transaction
import re
import json
from rest_framework.test import APIClient

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
            triangle = Shape.objects.create(
                name=shape_list[i], type=shape_list[i], user=user)
        self.assertEqual(Shape.objects.count(), len(shape_list))

        # check unique contraint
        with self.assertRaises(IntegrityError) as err:
            with transaction.atomic():
                Shape.objects.create(
                    name=shape_list[0], type=shape_list[0], user=user)
        self.assertTrue(re.match(r"unique", str(err.exception), re.IGNORECASE))

        # check update_or_create
        new_shape = Shape.objects.get(user=user, name=shape_list[0])
        new_shape.type = shape_list[1]
        new_shape.save()

        # check CASCADE delete
        user.delete()
        self.assertEqual(Shape.objects.count(), 0)

    def test_create_shape(self):
        username = 'quynt'
        password = '1'
        client = APIClient()
        UserTestCase.register_user(username, password)
        token = UserTestCase.login_user(username, password)
        # create
        response = client.post('/shapes/create', data={
            "name": "first_shape",
            "type": "triangle"
        }, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
        self.assertEqual(response.status_code, 201)
        # create
        response = client.post('/shapes/create', data={
            "name": "second_shape",
            "type": "triangle"
        }, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
        self.assertEqual(response.status_code, 201)
        # update
        response = client.post('/shapes/create', data={
            "name": "second_shape",
            "type": "diamond"
        }, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)

    def test_list(self):
        username = 'quynt'
        password = '1'
        client = APIClient()
        UserTestCase.register_user(username, password)
        token = UserTestCase.login_user(username, password)
        response = client.get('/shapes/',
                              **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        shapes = json.loads(response.content).get('shapes')
        self.assertEqual(len(shapes), 0)

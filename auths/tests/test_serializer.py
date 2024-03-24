from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from auths.serializers import UserSerializer


class UserSerializerTest(APITestCase):
    def test_serializer_validation(self):
        data = {
            "email": "test@test.com",
            "username": "test",
            "password": "password"

        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

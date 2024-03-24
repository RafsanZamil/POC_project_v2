from django.test import TestCase
from blogs.models import CustomUser


class CustomUserModelTest(TestCase):
    def test_create_user(self):
        email = "Test Title"
        username = "Test Username"
        password = "Test_password"

        user = CustomUser.objects.create_user(email=email, username=username, password=password)
        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertFalse(user.is_active)

        self.assertTrue(user.check_password(password))

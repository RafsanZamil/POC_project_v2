from auths.models import CustomUser
from blogs.models import Post
from django.test import TestCase


class PostModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword', is_active=str(True))

    def test_create_post(self):
        title = "Test Title"
        body = "Test Body"

        post = Post.objects.create(title=title, body=body, author=self.user)
        self.assertEqual(post.title, title)
        self.assertEqual(post.body, body)
        self.assertTrue(post.is_active)
        self.assertEqual(post.author, self.user)


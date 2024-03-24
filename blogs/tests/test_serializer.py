from rest_framework.test import APITestCase
from blogs.models import Post
from blogs.serializers import PostSerializer


class PostSerializerTest(APITestCase):
    def test_serializer_validation(self):
        data = {
            "title": "my title",
            "body": "body"


        }
        serializer = PostSerializer(data=data, partial=True)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

    def test_create(self):
        data = {
            "title": "my title",
            "body": "test",

        }
        serializer = PostSerializer(data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        post = serializer.create(serializer.validated_data)
        self.assertEqual(post.title, "my title")
        self.assertEqual(post.body, "test")
        self.assertTrue(post.is_active)

    def test_serializer_update_post(self):
        post = Post.objects.create(title="my title", body="my body")
        data = {
            "title": "new title"
        }

        serializer = PostSerializer(instance=post, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.update(post, serializer.validated_data)
        self.assertEqual(updated_user.title, "new title")


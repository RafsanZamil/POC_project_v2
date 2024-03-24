from django_rest.http import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import AccessToken
from auths.models import CustomUser
from blog_comments.models import Comment
from blogs.models import Post


class CreatePostTest(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword', is_active=True)
        self.token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_post(self):
        url = reverse('create_post')
        data = {'title': 'Test Post', 'body': 'This is a test post content'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'Test Post')


class ViewPostTest(APITestCase):
    def setUp(self):
        self.post = Post.objects.create(title="Test Post", body="This is a test post", id=1)
        self.comment1 = Comment.objects.create(post=self.post, content="Comment 1")
        self.comment2 = Comment.objects.create(post=self.post, content="Comment 2")

    def test_get_posts(self):
        pk = 1
        url = reverse('post_detail', args=[pk])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

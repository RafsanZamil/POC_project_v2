
# Create your models here.

from django.db import models
from POC_project_v2 import settings
from blogs.models import Post
from auths.models import CustomUser


# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True, default=None)
    comment_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, default=None)
    name = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    # def __str__(self):
    #     return f'Comment by {self.post} on {self.post}'
    #     pass
    #
    # pass



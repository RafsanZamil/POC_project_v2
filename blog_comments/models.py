from django.db import models
from blogs.models import Post
from auths.models import CustomUser


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE, null=True, default=None)
    comment_author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, default=None)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)



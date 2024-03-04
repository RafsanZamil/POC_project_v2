from django.db import models
from auths.models import CustomUser


class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    author = models.ForeignKey(CustomUser, related_name="books", on_delete=models.CASCADE, null=True,
                               default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(auto_created=True, null=True, default=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.title

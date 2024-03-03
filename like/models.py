from POC_project_v2 import settings
from django.db import models


# Create your models here.


class Like(models.Model):
    post = models.ForeignKey(settings.POST_MODEL, related_name="post", on_delete=models.CASCADE)
    liked_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="users", on_delete=models.CASCADE)

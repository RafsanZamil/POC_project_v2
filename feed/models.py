from django.db import models

from POC_project_v2 import settings


# Create your models here.

class FollowUser(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,  related_name="user", on_delete=models.CASCADE)
    followed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="follower", on_delete=models.CASCADE)


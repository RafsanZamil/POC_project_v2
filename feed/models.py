from django.db import models
from POC_project_v2 import settings


class FollowUser(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user", on_delete=models.CASCADE)
    followed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="follower", on_delete=models.CASCADE)


class Like(models.Model):
    post = models.ForeignKey(settings.POST_MODEL, related_name="post", on_delete=models.CASCADE)
    liked_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="users", on_delete=models.CASCADE)

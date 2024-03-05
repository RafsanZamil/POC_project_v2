from django.db import models
from blogs.models import Post
from auths.models import CustomUser
from blog_comments.models import Comment


class FollowUser(models.Model):
    user_id = models.ForeignKey(CustomUser, related_name="user", on_delete=models.CASCADE)
    followed_by = models.ForeignKey(CustomUser, related_name="follower", on_delete=models.CASCADE)


class Like(models.Model):
    post = models.ForeignKey(Post, related_name="post", on_delete=models.CASCADE)
    liked_by = models.ForeignKey(CustomUser, related_name="users", on_delete=models.CASCADE)


class ReactComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reacted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    Reaction_Choices = (
        ('H', 'HAHA'),
        ('S', 'SAD'),
        ('C', 'CARE'),
        ('L', 'LOVE')
    )
    reaction = models.CharField(max_length=1, choices=Reaction_Choices)

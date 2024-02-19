from rest_framework import serializers
from blog_comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("id", "post", "name", "body", "comment_author")
        model = Comment

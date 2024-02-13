from rest_framework import serializers

from blog_comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    # post = serializers.IntegerField(required=True)
    # comment_author = serializers.IntegerField(required=True)
    # body = serializers.CharField(required=True)
    # name = serializers.CharField(required=True)
    class Meta:
        fields = ("id","post","name","body","comment_author")
        model = Comment

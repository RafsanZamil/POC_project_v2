from rest_framework import serializers

from auths.models import CustomUser
from blog_comments.models import Comment
from blogs.models import Post


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    comment_author = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    name = serializers.CharField()
    body = serializers.CharField()

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.body = validated_data.get('body', instance.body)
        instance.post = validated_data.get('post', instance.post)
        instance.save()
        return instance

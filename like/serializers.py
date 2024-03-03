from rest_framework import serializers

from auths.models import CustomUser
from blogs.models import Post
from like.models import Like


class LikeSerializer(serializers.Serializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    liked_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    def create(self, validated_data):
        return Like.objects.create(**validated_data)

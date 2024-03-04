from rest_framework import serializers
from auths.models import CustomUser
from blog_comments.models import Comment
from blogs.models import Post
from feed.models import FollowUser, Like
from auths.serializers import UserSerializer
from blog_comments.serializers import CommentSerializer


class FollowSerializer(serializers.Serializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    followed_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    def create(self, validated_data):
        return FollowUser.objects.create(**validated_data)


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        extra_kwargs = {'is_active': {'write_only': True}}

    def to_representation(self, instance):
        response = super(PostCommentSerializer, self).to_representation(instance)
        response['author'] = UserSerializer(instance.author).data
        response['comment'] = CommentSerializer(Comment.objects.filter(post=instance), many=True).data
        return response


class LikeSerializer(serializers.Serializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    liked_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    def create(self, validated_data):
        return Like.objects.create(**validated_data)

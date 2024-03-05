from rest_framework import serializers
from auths.models import CustomUser
from blog_comments.models import Comment
from blogs.models import Post
from feed.models import FollowUser, Like, ReactComment
from blog_comments.serializers import  CommentFeedSerializer


class FollowSerializer(serializers.Serializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    followed_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    def create(self, validated_data):
        return FollowUser.objects.create(**validated_data)


class ReactSerializer(serializers.Serializer):
    comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all())
    reacted_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    reaction = serializers.CharField()

    def create(self, validated_data):
        return ReactComment.objects.create(**validated_data)


class LikeSerializer(serializers.Serializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    liked_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    def create(self, validated_data):
        return Like.objects.create(**validated_data)


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "body", "created_at", "updated_at"]
        extra_kwargs = {'is_active': {'write_only': True}}

    def to_representation(self, instance):
        response = super(PostCommentSerializer, self).to_representation(instance)
        author = (CustomUser.objects.filter(id=instance.author.id).values_list("username", flat=True))
        response['blog author'] = author[0]
        response['total likes'] = Like.objects.filter(post=instance).count()
        response['comment'] = CommentFeedSerializer(Comment.objects.filter(post=instance), many=True).data
        return response

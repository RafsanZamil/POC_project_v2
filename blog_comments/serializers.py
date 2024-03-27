from rest_framework import serializers

from auths.models import CustomUser
from blog_comments.models import Comment
from feed.models import ReactComment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "comment_author", "content"]


class CommentCacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["content"]


class CommentFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', ]

    def to_representation(self, instance):
        response = super(CommentFeedSerializer, self).to_representation(instance)
        author = CustomUser.objects.filter(id=instance.comment_author.id).values_list("username", flat=True)
        response['comment Author'] = author[0]
        response['total reacts'] = ReactComment.objects.filter(comment=instance).count()
        response['haha reacts'] = ReactComment.objects.filter(comment=instance, reaction="H").count()
        response['sad reacts'] = ReactComment.objects.filter(comment=instance, reaction="S").count()
        response['care reacts'] = ReactComment.objects.filter(comment=instance, reaction="C").count()
        response['love reacts'] = ReactComment.objects.filter(comment=instance, reaction="L").count()
        return response

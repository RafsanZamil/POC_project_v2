from rest_framework import serializers

from auths.models import CustomUser
from feed.models import FollowUser


class FollowSerializer(serializers.Serializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    followed_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    def create(self, validated_data):
        return FollowUser.objects.create(**validated_data)

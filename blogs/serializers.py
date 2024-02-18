from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id",
                  "author",
                  "title",
                  "body",
                  "created_at",
                  "is_active"
                  )

        model = Post

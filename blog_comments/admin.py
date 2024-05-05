from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ["post", "comment_author", "content"]
    readonly_fields = []


admin.site.register(Comment, CommentAdmin)

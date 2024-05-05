from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "body", "author"]
    readonly_fields = []


admin.site.register(Post, PostAdmin)

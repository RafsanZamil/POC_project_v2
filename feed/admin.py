from django.contrib import admin

from .models import FollowUser, ReactComment

admin.site.register(ReactComment)

admin.site.register(FollowUser)

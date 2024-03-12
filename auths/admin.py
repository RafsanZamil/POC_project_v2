from django.contrib import admin

from auths.models import CustomUser

admin.site.register(CustomUser)


class ConcertAdmin(admin.ModelAdmin):
    list_display = ["name", ]
    readonly_fields = []

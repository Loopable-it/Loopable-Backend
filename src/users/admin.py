from django.contrib import admin

from users.models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'lastname', 'type', 'is_verified')
    readonly_fields = ('sign_in_provider', 'created_at', 'updated_at')

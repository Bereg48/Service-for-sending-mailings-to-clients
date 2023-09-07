from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'country', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('country', 'is_active', 'is_staff', 'is_superuser')
    list_display_links = ('id', 'email',)
    readonly_fields = ('token', 'last_login', 'date_joined')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Информация', {'fields': ('first_name', 'last_name', 'country', 'token')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2')}),
    )
    ordering = ('id', 'email',)


admin.site.unregister(Group)

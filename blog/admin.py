from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'view_count', 'image')
    search_fields = ('title',)
    list_filter = ('view_count',)

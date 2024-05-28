from django.contrib import admin

from resource_library.models import Resource


# Register your models here.

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'source', 'related_lesson', 'added_at')

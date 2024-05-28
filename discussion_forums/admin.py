from django.contrib import admin

from .models import Topic, Comment, CommentDeletionEvent


# Register your models here

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'created_at')  # Customize displayed fields


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('message', 'topic', 'created_by', 'created_at')  # Customize displayed fields


@admin.register(CommentDeletionEvent)
class CommentDeletionEventAdmin(admin.ModelAdmin):
    list_display = ('comment', 'deleted_by', 'deletion_time')

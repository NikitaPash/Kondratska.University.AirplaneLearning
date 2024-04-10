from django.db import models
from django.contrib.auth.models import User

from modules.models import Lesson
from profile_page.models import Profile


class Topic(models.Model):
    title = models.CharField(max_length=50)
    subject = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    description = models.TextField()
    starter = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    message = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.created_by.username} on post: {self.topic}"

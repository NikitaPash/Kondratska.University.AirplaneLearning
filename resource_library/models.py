from django.db import models

from modules.models import Lesson


# Create your models here.

class Resource(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=[("Article", "Article"), ("Video", "Video"), ("Other", "Other")],
                            default="Other")
    related_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='related_lesson')
    description = models.TextField(default="Description is flying to us...")
    source = models.URLField(max_length=500)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

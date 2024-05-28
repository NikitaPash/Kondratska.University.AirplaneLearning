from django.db import models

from profile_page.models import Profile


# Create your models here.

class Feedback(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=50, choices=[('Positive', 'Positive'), ('Negative', 'Negative')])
    description = models.TextField()
    screenshot = models.ImageField(upload_to='feedback/screenshots')

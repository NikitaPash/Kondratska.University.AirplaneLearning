import os
import random
import string

from django.contrib.auth.models import AbstractUser, User
from django.db import models

from modules.models import Language


def get_upload_path(instance, filename):
    return os.path.join('uploads', filename)


def generate_random_password(length=12):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


def get_random_profile_pic():
    profile_pics = [
        'plushik_flower.png',
        'plushik_knife.png'
    ]
    return random.choice(profile_pics)


class LearnerType(models.Model):
    title = models.CharField(max_length=50)
    alternate_title = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title


class Profile(AbstractUser):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    progress = models.FloatField(default=0)
    profile_pic_url = models.ImageField(upload_to='uploads/', default=get_random_profile_pic, unique=False)
    learner_type = models.ForeignKey(LearnerType, on_delete=models.CASCADE, unique=False, default=0)
    chosen_language = models.ForeignKey(Language, on_delete=models.CASCADE, unique=False, default=0)
    receive_notifications = models.CharField(max_length=50, choices=[('Send', 'Send'), ('Do not send', 'Do not send')],
                                             default='Send')
    new_modules_notifications = models.CharField(max_length=50,
                                                 choices=[('Send', 'Send'), ('Do not send', 'Do not send')],
                                                 default='Send')
    quiz_results_notifications = models.CharField(max_length=50,
                                                  choices=[('Send', 'Send'), ('Do not send', 'Do not send')],
                                                  default='Send')
    discussion_notifications = models.CharField(max_length=50,
                                                choices=[('Send', 'Send'), ('Do not send', 'Do not send')],
                                                default='Send')
    new_resources_notifications = models.CharField(max_length=50,
                                                   choices=[('Send', 'Send'), ('Do not send', 'Do not send')],
                                                   default='Send')
    groups = models.ManyToManyField('auth.Group', related_name='profile_set')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='profile_set')

    def __str__(self):
        return self.email

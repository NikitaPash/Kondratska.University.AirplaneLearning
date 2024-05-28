from django.db import models
from django.utils.translation import gettext_lazy as _

from modules.models import Lesson, Quiz, Question
from profile_page.models import Profile


class LessonStatus(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Not Started', _('Not Started')),
            ('In Progress', _('In Progress')),
            ('Completed', _('Completed')),
        ],
        default='not_started',
    )
    finished_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status


class QuizStatus(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Not Started', _('Not Started')),
            ('In Progress', _('In Progress')),
            ('Completed', _('Completed')),
        ],
        default='Not Started',
    )
    finished_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status


class QuizUserAnswers(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user_answer = models.TextField()
    is_correct = models.CharField(max_length=15, choices=[("Y", "Correct"), ("N", "Incorrect")], default="Incorrect")

    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_answer

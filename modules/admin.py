from django.contrib import admin

from .models import Language, Lesson, Quiz, Module, Section, Question, Answer
from .user_progress_models import LessonStatus, QuizStatus, QuizUserAnswers

# Register your models here

admin.site.register(Language)
admin.site.register(Lesson)
admin.site.register(Quiz)
admin.site.register(Module)
admin.site.register(Section)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(LessonStatus)
admin.site.register(QuizStatus)
admin.site.register(QuizUserAnswers)

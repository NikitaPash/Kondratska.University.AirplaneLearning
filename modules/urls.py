from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from modules import views

urlpatterns = [
    path("", views.all_possible_classes, name="all_possible_classes"),
    path("modules_list/<int:language_id>/", views.modules_list, name='modules_list'),
    path("modules_list/<int:language_id>/lesson_info/<int:lesson_id>/", views.lesson_info, name='lesson_info'),
    path("modules_list/<int:language_id>/lesson_quiz/<int:lesson_id>/", views.lesson_quiz, name='lesson_quiz'),
]

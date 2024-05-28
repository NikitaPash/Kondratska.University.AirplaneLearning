from django.urls import path

from modules import views

urlpatterns = [
    path("", views.all_possible_classes, name="all_possible_classes"),
    path("modules_list/<int:language_id>/", views.modules_list, name='modules_list'),
    path("modules_list/<int:language_id>/lesson/<int:lesson_id>/", views.lesson_info, name='lesson_info'),
    path("modules_list/<int:language_id>/quiz/<int:quiz_id>/", views.lesson_quiz, name='lesson_quiz'),
    path("modules_list/<int:language_id>/quiz/<int:quiz_id>/result/", views.quiz_result, name='quiz_result'),
]

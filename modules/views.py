from django import template
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Language, Lesson, Question, Answer, Quiz



def all_possible_classes(request):
    languages = Language.objects.all()
    context = {
        'languages': languages
    }
    return render(request, 'modules_main.html', context)


def modules_list(request, language_id):
    language = get_object_or_404(Language, pk=language_id)
    modules = language.module_set.all()
    lessons = Lesson.objects.filter(module__language=language)
    quizzes = Quiz.objects.filter(module__language=language)

    context = {
        'language': language,
        'modules': modules,
        'lessons': lessons,
        'quizzes': quizzes,
    }
    return render(request, 'modules_list.html', context)


def lesson_info(request, lesson_id, language_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    language = get_object_or_404(Language, pk=language_id)
    sections = lesson.section_set.all()
    section_count = sections.count()
    context = {'lesson': lesson, 'language': language, 'sections': sections, 'section_count': section_count}
    complete_lesson(request, lesson_id)
    return render(request, 'lesson_info.html', context)


def lesson_quiz(request, quiz_id, language_id):
    quiz = get_object_or_404(Lesson, pk=quiz_id)
    language = get_object_or_404(Language, pk=language_id)
    questions = Question.objects.filter(quiz_id=quiz_id)
    answers = Answer.objects.filter(question__in=questions)
    complete_quiz(request, quiz_id)
    return render(request, 'lesson_quiz.html',
                  {'quiz': quiz, 'language': language, 'questions': questions, 'answers': answers})


def complete_lesson(request, lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    lesson.status = 'Completed'
    lesson.save()


def complete_quiz(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    quiz.status = 'Completed'
    quiz.save()


from django.shortcuts import render
from .models import Question


def quiz_result(request, language_id, quiz_id):
    questions = Question.objects.all()

    quiz_data = {}

    for question in questions:
        correct_answer = question.answer_set.filter(is_correct='Correct').first()
        quiz_data[question] = correct_answer

    context = {'quiz_data': quiz_data}

    return render(request, 'quiz_result.html', context)




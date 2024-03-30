import os

from azure.storage.blob import BlobServiceClient
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from profile_page.forms import LearnerTypeSettings, ProfilePictureSettings
from profile_page.models import Profile, get_random_profile_pic
from modules.models import Lesson, Quiz
from modules.user_progress_models import LessonStatus, QuizStatus, QuizUserAnswers


def get_latest_lesson_and_quiz(profile):
    latest_lesson_status = LessonStatus.objects.filter(profile=profile, status='Completed').order_by(
        '-finished_at').first()
    latest_quiz_status = QuizStatus.objects.filter(profile=profile, status='Completed').order_by('-finished_at').first()
    return latest_lesson_status.lesson if latest_lesson_status else None, latest_quiz_status.quiz if latest_quiz_status else None


def calculate_progress(user_profile):
    total_lessons = len(list(Lesson.objects.all()))
    total_quizzes = len(list(Quiz.objects.all()))

    completed_lessons = LessonStatus.objects.filter(profile=user_profile, status="Completed").count()
    completed_quizzes = QuizStatus.objects.filter(profile=user_profile, status="Completed").count()

    total_items = total_lessons + total_quizzes
    completed_items = completed_lessons + completed_quizzes

    if total_items > 0:
        progress_percentage = (completed_items / total_items) * 100
    else:
        progress_percentage = 0

    user_profile.progress = progress_percentage
    user_profile.save()


@login_required
def profile_page(request):
    try:
        student = Profile.objects.get(user=request.user)
        calculate_progress(student)
    except Profile.DoesNotExist:
        new_profile = Profile.objects.create(user=request.user, username=request.user.username,
                                             email=request.user.email,
                                             user_id=request.user.id)
        student = new_profile
        calculate_progress(student)

    latest_lesson = LessonStatus.objects.filter(profile=student, status='Completed').order_by('-finished_at').first()
    latest_quiz = QuizStatus.objects.filter(profile=student, status='Completed').order_by('-finished_at').first()

    latest_lesson_language = latest_lesson.lesson.module.language if latest_lesson else None
    latest_quiz_language = latest_quiz.quiz.module.language if latest_quiz else None

    azure_storage_connection_string = os.getenv("connection_str")
    container_name = "pfpcontainer"
    blob_name = student.profile_pic_url

    blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    profile_picture_url = blob_client.url

    return render(request, 'profile_page.html', {'student': student, 'user': request.user,
                                                 'latest_lesson': latest_lesson, 'latest_quiz': latest_quiz,
                                                 'latest_lesson_language': latest_lesson_language,
                                                 'latest_quiz_language': latest_quiz_language,
                                                 'profile_picture_url': profile_picture_url})


@login_required
def profile_settings(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if 'learner_type_submit' in request.POST:
            learner_type_form = LearnerTypeSettings(request.POST, instance=profile)
            if learner_type_form.is_valid():
                learner_type_form.save()
                return redirect('profile_page')
            else:
                print(learner_type_form.errors)

        elif 'profile_pic_submit' in request.POST:
            profile_pic_form = ProfilePictureSettings(request.POST, request.FILES, instance=profile)
            if profile_pic_form.is_valid():
                profile_pic_form.instance.container_name = 'pfpcontainer'  # Set the container name
                profile_pic_form.save()
                return redirect('profile_page')

        elif 'default_profile_pic' in request.POST:
            profile.profile_pic_url = get_random_profile_pic()
            profile.save()
            return redirect('profile_page')

    learner_type_form = LearnerTypeSettings(instance=profile)
    profile_pic_form = ProfilePictureSettings(instance=profile)

    return render(request, 'profile_settings.html', {
        'learner_type_form': learner_type_form,
        'profile_pic_form': profile_pic_form
    })


@login_required()
def logout_page(request):
    logout(request)
    return redirect('/')

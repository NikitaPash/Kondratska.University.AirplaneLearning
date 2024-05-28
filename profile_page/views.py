import os

from azure.storage.blob import BlobServiceClient
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from opentelemetry import trace
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from discussion_forums.utils import load_profanity_words
from modules.models import Lesson, Quiz, Module
from modules.user_progress_models import LessonStatus, QuizStatus
from profile_page.forms import LearnerTypeSettings, ProfilePictureSettings, NotificationSettings
from profile_page.models import Profile, get_random_profile_pic, LearnerType
from ALPP.swagger import StudentSerializer

PROFANE_WORDS = load_profanity_words('profanity.txt')
tracer = trace.get_tracer(__name__)


def get_latest_lesson_and_quiz(profile):
    latest_lesson_status = LessonStatus.objects.filter(profile=profile, status='Completed').order_by(
        '-finished_at').first()
    latest_quiz_status = QuizStatus.objects.filter(profile=profile, status='Completed').order_by('-finished_at').first()
    return latest_lesson_status.lesson if latest_lesson_status else None, latest_quiz_status.quiz if latest_quiz_status else None


def calculate_progress(user_profile, chosen_language_id):
    total_modules = Module.objects.filter(language_id=chosen_language_id)
    total_lessons = Lesson.objects.filter(module__in=total_modules).count()
    total_quizzes = Quiz.objects.filter(module__in=total_modules).count()

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
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_page(request, username):
    with tracer.start_as_current_span("profile_page") as span:
        student = get_student_profile(username)
        if not student:
            if 'setup' not in request.path:
                return redirect("setup")

        calculate_progress(student, student.chosen_language_id)

        latest_lesson, latest_lesson_language = get_latest_completed_lesson(student)
        latest_quiz, latest_quiz_language = get_latest_completed_quiz(student)

        profile_picture_url = get_profile_picture_url(student.profile_pic_url)

        serializer = StudentSerializer(student)

        data = {
            'student': serializer.data
        }

        if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
            return Response(data, status=status.HTTP_200_OK)
        else:
            return render(request, 'profile/profile_page.html', {'student': student, 'user': request.user,
                                                                 'latest_lesson': latest_lesson,
                                                                 'latest_quiz': latest_quiz,
                                                                 'latest_lesson_language': latest_lesson_language,
                                                                 'latest_quiz_language': latest_quiz_language,
                                                                 'profile_picture_url': profile_picture_url})


def get_student_profile(username):
    try:
        user = User.objects.get(username=username)
        return Profile.objects.get(user=user)
    except (User.DoesNotExist, Profile.DoesNotExist):
        return None


def get_latest_completed_lesson(student):
    latest_lesson = LessonStatus.objects.filter(profile=student, status='Completed').order_by('-finished_at').first()
    latest_lesson_language = latest_lesson.lesson.module.language if latest_lesson else None
    return latest_lesson, latest_lesson_language


def get_latest_completed_quiz(student):
    latest_quiz = QuizStatus.objects.filter(profile=student, status='Completed').order_by('-finished_at').first()
    latest_quiz_language = latest_quiz.quiz.module.language if latest_quiz else None
    return latest_quiz, latest_quiz_language


def get_profile_picture_url(profile_pic_url):
    azure_storage_connection_string = os.getenv("connection_str")
    container_name = "pfpcontainer"
    blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=profile_pic_url)

    profile_picture_url = blob_client.url
    return profile_picture_url


@login_required
def profile_settings(request):
    with tracer.start_as_current_span("profile_settings") as span:
        profile = Profile.objects.get(user=request.user)
        learner_types = LearnerType.objects.all()

        if request.method == 'POST':
            if 'learner_type_submit' in request.POST:
                learner_type_form = LearnerTypeSettings(request.POST, instance=profile)
                if learner_type_form.is_valid():
                    learner_type_form.save()

            elif 'profile_pic_submit' in request.POST:
                profile_pic_form = ProfilePictureSettings(request.POST, request.FILES, instance=profile)
                if profile_pic_form.is_valid():
                    profile_pic_form.instance.container_name = 'pfpcontainer'
                    profile_pic_form.save()

            elif 'default_profile_pic' in request.POST:
                profile.profile_pic_url = get_random_profile_pic()
                profile.save()

            elif 'receive_notifications_submit' in request.POST:
                data = request.POST.copy()
                for field_name in [
                    'receive_notifications',
                    'new_modules_notifications',
                    'quiz_results_notifications',
                    'discussion_notifications',
                    'new_resources_notifications',

                ]:
                    data.setdefault(field_name, 'Do not send')
                receive_notifications_form = NotificationSettings(data, instance=profile)
                if receive_notifications_form.is_valid():
                    receive_notifications_form.save()

        learner_type_form = LearnerTypeSettings(instance=profile)
        profile_pic_form = ProfilePictureSettings(instance=profile)
        receive_notifications_form = NotificationSettings(instance=profile)

        return render(request, 'profile/profile_settings.html', {
            'learner_type_form': learner_type_form,
            'profile_pic_form': profile_pic_form,
            'receive_notifications_form': receive_notifications_form,
            'learner_types': learner_types
        })


@login_required()
def logout_page(request):
    with tracer.start_as_current_span("logout_page") as span:
        logout(request)
        return redirect('/')

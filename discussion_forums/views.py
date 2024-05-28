import os
import re
from datetime import datetime

from azure.storage.blob import BlobServiceClient
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags import humanize
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from opentelemetry import trace
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from discussion_forums.models import Topic, Comment, CommentDeletionEvent
from discussion_forums.utils import contains_profanity, PROFANE_WORDS
from modules.models import Module, Lesson

tracer = trace.get_tracer(__name__)


@login_required
def main_forum_page(request):
    with tracer.start_as_current_span("main_forum_page") as span:
        modules_for_topics = Module.objects.filter(language=request.user.profile.chosen_language)
        lessons_for_topics = Lesson.objects.filter(module__in=modules_for_topics)
        topics_for_lessons = Topic.objects.filter(subject__in=lessons_for_topics)
        all_topics = topics_for_lessons.order_by('-created_at')
        is_admin = request.user.is_superuser
        return render(request, "forums/main_forum_page.html", {'all_topics': all_topics, 'is_admin': is_admin})


@login_required
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def topic_page(request, topic_id):
    with tracer.start_as_current_span("topic_page") as span:
        topic = get_object_or_404(Topic, pk=topic_id)
        is_admin = request.user.is_superuser

        all_comments = Comment.objects.filter(topic_id=topic_id).order_by("-created_at")
        profile_pictures = {comment.created_by.username: get_profile_pic_url(comment.created_by) for comment in
                            all_comments}

        for comment in all_comments:
            comment.humanized_created_at = humanize.naturaltime(comment.created_at)

        if request.method == 'POST':
            comment_text = request.POST.get('comment_text')
            message = None

            if not comment_text:
                message = 'Comment cannot be empty.'
            elif contains_profanity(comment_text, PROFANE_WORDS):
                message = 'Your comment contains something inappropriate.'
            elif len(comment_text) > 500:
                message = 'Your comment is too long! Make sure it is less than 500 symbols.'

            if message:
                return render(request, 'forums/topic_page.html',
                              {'topic': topic, 'all_comments': all_comments,
                               'profile_pictures': profile_pictures, 'is_admin': is_admin, 'request': request})

            Comment.objects.create(
                message=comment_text,
                topic=topic,
                created_by=request.user.profile,
                created_at=datetime.now()
            )
            send_reply_notification_email(request.user.profile, comment_text)
            return redirect('topic_page', topic_id=topic_id)

        if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
            data = {
                'topic': {
                    'id': topic.id,
                    'title': topic.title,
                    'description': topic.description,
                    'created_at': topic.created_at,
                },
                'comments': [{
                    'message': comment.message,
                    'created_by': comment.created_by.username,
                    'created_at': comment.humanized_created_at
                } for comment in all_comments],
                'profile_pictures': profile_pictures,
                'is_admin': is_admin
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return render(request, 'forums/topic_page.html',
                          {'topic': topic, 'all_comments': all_comments,
                           'profile_pictures': profile_pictures, 'is_admin': is_admin, 'request': request})


def send_reply_notification_email(comment, comment_text):
    mentioned_usernames = re.findall(r'@(\w+)', comment_text)
    for username in mentioned_usernames:
        try:
            user = User.objects.get(username=username)
            if user.profile.discussion_notifications == "Send":
                recipient_email = user.email
                subject = 'You have been mentioned in a comment'
                context = {'user': user, 'comment': comment}
                html_message = render_to_string('emails/email_mention_notification.html', context)
                plain_message = strip_tags(html_message)
                send_mail(subject, plain_message, None, [recipient_email], html_message=html_message)
        except User.DoesNotExist:
            pass


def get_profile_pic_url(student):
    with tracer.start_as_current_span("get_profile_pic_url") as span:
        azure_storage_connection_string = os.getenv("connection_str")
        container_name = "pfpcontainer"
        blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=student.profile_pic_url)
        profile_pic_url = blob_client.url
        return profile_pic_url


def delete_comment(request, comment_id):
    with tracer.start_as_current_span("delete_comment") as span:
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.method == 'POST':
            if request.user == comment.created_by.user or request.user.is_superuser:
                com_event = CommentDeletionEvent.objects.create(comment=comment, deleted_by=request.user,
                                                                deletion_time=datetime.now())
                com_event.save()
                send_comment_deletion_notification(com_event)
                comment.delete()
                return redirect('topic_page', topic_id=comment.topic_id)
        return redirect('topic_page', topic_id=comment.topic_id)


def send_comment_deletion_notification(com_ev):
    with tracer.start_as_current_span("send_comment_deletion_notification") as span:
        if com_ev.comment.created_by.discussion_notifications == "Send":
            if com_ev.deleted_by.is_superuser:
                subject = "Your comment... was..."
                html_message = render_to_string('emails/email_comment_deletion.html', {'comment': com_ev.comment})
                plain_message = strip_tags(html_message)
                user_to_notify = com_ev.comment.created_by.email

                send_mail(subject, plain_message, None, [user_to_notify], html_message=html_message)

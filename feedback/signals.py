from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Feedback


@receiver(post_save, sender=Feedback)
def send_feedback_notification(sender, instance, created, **kwargs):
    if created:
        print("Sending mail...")
        subject = 'New Feedback Submitted'
        blob_storage_base_url = "https://alpolyprostorage.blob.core.windows.net/"
        screenshot_blob_url = f"{blob_storage_base_url}{settings.AZURE_CONTAINER}/{instance.screenshot}"

        context = {
            'feedback_id': instance.pk,
            'profile': instance.profile,
            'feedback_type': instance.feedback_type,
            'description': instance.description,
            'screenshot': screenshot_blob_url if instance.screenshot else None,
        }
        html_message = render_to_string('emails/email_feedback.html', context)
        plain_message = strip_tags(html_message)
        admins = User.objects.filter(is_superuser=True)
        recipient_list = [admin.email for admin in admins]
        send_mail(subject, plain_message, None, recipient_list, html_message=html_message)

        if instance.profile.receive_notifications == "Send":
            user_subject = 'Feedback Submission Confirmation'
            user_context = {
                'feedback_id': instance.pk,
            }
            user_html_message = render_to_string('emails/email_feedback_confirmation.html', user_context)
            user_plain_message = strip_tags(user_html_message)
            user_email = instance.profile.email
            send_mail(user_subject, user_plain_message, None, [user_email], html_message=user_html_message)

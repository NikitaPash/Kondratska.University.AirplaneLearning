from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from profile_page.models import Profile
from .models import Module


@receiver(post_save, sender=Module)
def send_module_notification(sender, instance, created, **kwargs):
    if created:
        subject = "New Module Added"
        html_message = render_to_string('emails/email_new_module.html', {'module': instance})
        plain_message = strip_tags(html_message)

        users_to_notify = Profile.objects.filter(chosen_language_id=instance.language.id,
                                                 new_modules_notifications="Send")
        recipient_list = [user.user.email for user in users_to_notify]

        send_mail(subject, plain_message, None, recipient_list, html_message=html_message)

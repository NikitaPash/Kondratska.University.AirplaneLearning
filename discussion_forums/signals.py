from django.db.models.signals import post_save
from django.dispatch import receiver

from discussion_forums.models import Topic
from modules.models import Lesson


@receiver(post_save, sender=Lesson)
def create_discussion_topic(sender, instance, created, **kwargs):
    if created:
        content = f"Here, you will discuss your experience on learning {instance.title}"
        Topic.objects.create(
            title=instance.title,
            subject=instance,
            description=content,
        )

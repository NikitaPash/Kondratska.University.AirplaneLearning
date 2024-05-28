from django.core.management.base import BaseCommand

from discussion_forums.models import Topic
from modules.models import Lesson


class Command(BaseCommand):
    help = 'Creates topics for all lessons'

    def handle(self, *args, **kwargs):
        for lesson in Lesson.objects.all():
            existing_topic = Topic.objects.filter(subject=lesson).first()
            if existing_topic:
                self.stdout.write(self.style.WARNING(f"A topic with the subject '{lesson}' already exists. "
                                                     f"Skipping creation for lesson '{lesson.title}'"))
            else:
                content = f"Here, you will discuss your experience on learning {lesson.title}."
                Topic.objects.create(
                    title=lesson.title,
                    subject=lesson,
                    description=content,
                )
                self.stdout.write(self.style.SUCCESS(f"Topic created for lesson '{lesson.title}'"))

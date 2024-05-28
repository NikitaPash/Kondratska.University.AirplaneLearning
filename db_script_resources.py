import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ALPP.settings")

import django

django.setup()

from faker import Faker
from modules.models import Lesson
from resource_library.models import Resource

fake = Faker()


def create_resources(num_resources=30, lessons=None):
    resources = []
    if not lessons:
        lessons = Lesson.objects.all()
    for i in range(1, num_resources + 1):
        resource = Resource.objects.create(
            name=f"Resource #{i}",
            type=fake.random_element(["Article", "Video", "Other"]),
            related_lesson=fake.random_element(lessons),
            description=fake.paragraph(),
            source=fake.url()
        )
        resources.append(resource)
    return resources


def main():
    lessons = Lesson.objects.all()
    resources = create_resources(lessons=lessons)


if __name__ == "__main__":
    main()

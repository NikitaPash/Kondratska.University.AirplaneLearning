from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from modules.models import Lesson, Language, Module
from profile_page.models import Profile, LearnerType
from resource_library.models import Resource


class ResourcesViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.language = Language.objects.create(name='Test Lan', joke='Test Lan')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.learner_type = LearnerType.objects.create(title='Test Learner Type')
        self.profile = Profile.objects.create(user=self.user, chosen_language_id=self.language.id,
                                              learner_type_id=self.learner_type.id)
        self.client.login(username='testuser', password='testpassword')
        self.module = Module.objects.create(title='Test Module', language=self.language)
        self.lesson = Lesson.objects.create(title='Test Lesson', module=self.module)
        self.resource = Resource.objects.create(
            name='Test Resource',
            related_lesson=self.lesson,
            description='Test Description',
            added_at=timezone.now(),
            source="I made it up"
        )
        self.url = reverse('resources')

    @patch('django.contrib.staticfiles.storage.staticfiles_storage.url', return_value='/leeri_logo.png')
    def test_resources_view(self, mock_url):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.resource.name)
        self.assertContains(response, self.resource.source)


class DictionaryViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.language = Language.objects.create(name='Test Lan', joke='Test Lan')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.learner_type = LearnerType.objects.create(title='Test Learner Type')
        self.profile = Profile.objects.create(user=self.user, chosen_language_id=self.language.id,
                                              learner_type_id=self.learner_type.id)
        self.client.login(username='testuser', password='testpassword')
        self.url = reverse('dictionary')
        self.profanity_word = 'fuck'
        self.non_profanity_word = 'book'

    @patch('django.contrib.staticfiles.storage.staticfiles_storage.url', return_value='/leeri_logo.png')
    def test_dictionary_view_get(self, mock_url):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    @patch('django.contrib.staticfiles.storage.staticfiles_storage.url', return_value='/leeri_logo.png')
    def test_dictionary_view_post_with_valid_word(self, mock_url):
        data = {'word': self.non_profanity_word}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.non_profanity_word)

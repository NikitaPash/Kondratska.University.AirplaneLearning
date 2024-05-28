from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from django.urls import reverse

from modules.models import Language
from profile_page.models import Profile, LearnerType
from .views import register, language_and_learning_path_selection


class RegisterViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_register_unauthenticated_user(self):
        request = self.factory.get(reverse('register'))
        request.user = AnonymousUser()

        response = register(request)

        print("User successfully created")

        self.assertEqual(response.status_code, 200)


class LanguageAndLearningPathSelectionTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.chosen_language = Language.objects.create(name='English')
        self.learner_type = LearnerType.objects.create(title='Beginner')

    def test_language_and_learning_path_selection_post(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password')

        data = {'chosen_language': self.chosen_language.pk, 'learner_type': self.learner_type.pk}
        request = self.factory.post(reverse('setup'), data=data)
        request.user = user

        response = language_and_learning_path_selection(request)

        profile_exists = Profile.objects.filter(user=user).exists()
        if not profile_exists:
            print("Profile creation failed. Details:")
            print("User:", user)
            print("Response content:", response.content.decode())
            print("Form errors:", response.context_data['form'].errors if hasattr(response, 'context_data') else None)

        self.assertTrue(profile_exists)

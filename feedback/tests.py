from django.contrib.auth.models import User
from django.test import TestCase

from modules.models import Language
from profile_page.models import LearnerType, Profile


class FeedbackViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.language = Language.objects.create(name='Test Lan', joke='Test Lan')
        self.learner_type = LearnerType.objects.create(title='Test Learner Type')
        self.profile = Profile.objects.create(user=self.user, chosen_language_id=self.language.id,
                                              learner_type_id=self.learner_type.id)
        self.url = '/feedback/'

    def test_feedback(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {
            'feedback_type': 'Positive',
            'description': 'Test description',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Form filled out successfully!")

    def test_feedback_with_invalid_form(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {'invalid_field': 'invalid_value'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Form filled out successfully!")

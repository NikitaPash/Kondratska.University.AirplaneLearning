from unittest.mock import MagicMock, patch

from django.shortcuts import reverse
from django.test import TestCase


class ProfilePageTestCase(TestCase):
    @patch('profile_page.views.get_student_profile')
    @patch('profile_page.views.get_latest_completed_lesson')
    @patch('profile_page.views.get_latest_completed_quiz')
    @patch('profile_page.views.get_profile_picture_url')
    def test_profile_page_view(self, mock_get_profile_picture_url, mock_get_latest_completed_quiz,
                               mock_get_latest_completed_lesson, mock_get_student_profile):
        dummy_user = MagicMock()
        dummy_profile = MagicMock()

        mock_get_student_profile.return_value = dummy_profile
        mock_get_latest_completed_lesson.return_value = (None, None)
        mock_get_latest_completed_quiz.return_value = (None, None)
        mock_get_profile_picture_url.return_value = "http://example.com/profile_pic.jpg"

        response = self.client.get(reverse('profile_page'))

        self.assertEqual(response.status_code, 302)

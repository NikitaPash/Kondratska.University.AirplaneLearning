import unittest
from unittest.mock import patch, MagicMock

from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase

from modules.signals import send_module_notification
from modules.views import complete_lesson, complete_quiz
from profile_page.models import Profile
from .models import Language, Module, Lesson, Quiz
from .user_progress_models import LessonStatus, QuizStatus


class LessonCompletionTestCase(TestCase):

    def setUp(self):
        self.language = Language.objects.create(name='Test Language')
        self.module = Module.objects.create(title='Test Module', language=self.language)
        self.lesson = Lesson.objects.create(title='Test Lesson', module=self.module)
        self.user = User.objects.create(username='testuser')
        self.profile = Profile.objects.create(user=self.user)
        self.lesson_status = LessonStatus.objects.create(lesson=self.lesson, profile=self.profile, status='Not Started')

    @patch('modules.views.complete_lesson')
    def test_complete_lesson(self, mock_complete_lesson):
        mock_complete_lesson.return_value = None
        request_factory = RequestFactory()
        request = request_factory.get('/')
        request.user = self.user
        self.assertEqual(self.lesson_status.status, 'Not Started')
        complete_lesson(request, self.lesson.id)
        self.lesson_status.refresh_from_db()
        self.assertEqual(self.lesson_status.status, 'Completed')
        print(f"Lesson {self.lesson.title} is {self.lesson_status.status}!")


class QuizCompletionTestCase(TestCase):

    def setUp(self):
        self.language = Language.objects.create(name='Test Language')
        self.module = Module.objects.create(title='Test Module', language=self.language)
        self.quiz = Quiz.objects.create(title='Test Quiz', module=self.module)
        self.user = User.objects.create(username='testuser')
        self.profile = Profile.objects.create(user=self.user)
        self.quiz_status = QuizStatus.objects.create(quiz=self.quiz, profile=self.profile, status='Not Started')

    @patch('modules.views.complete_quiz')
    def test_complete_quiz(self, mock_complete_quiz):
        mock_complete_quiz.return_value = None
        request_factory = RequestFactory()
        request = request_factory.get('/')
        request.user = self.user
        self.assertEqual(self.quiz_status.status, 'Not Started')
        complete_quiz(request, self.quiz.id)
        self.quiz_status.refresh_from_db()
        self.assertEqual(self.quiz_status.status, 'Completed')
        print(f"Quiz {self.quiz.title} is {self.quiz_status.status}!")


class TestSendModuleNotification(TestCase):
    def setUp(self):
        self.language = Language.objects.create(name="Test Language", joke="Test Joke")
        self.module = Module.objects.create(title='Test Module',
                                            language=self.language)  # Example module object creation

    @patch('modules.signals.render_to_string')
    @patch('modules.signals.send_mail')
    @patch('modules.signals.Profile.objects.filter')
    def test_send_module_notification(self, mock_filter, mock_send_mail, mock_render_to_string):
        mock_profile = MagicMock()
        mock_profile.user.email = 'test@example.com'
        mock_filter.return_value = [mock_profile]
        mock_render_to_string.return_value = '<html><body>Test</body></html>'

        send_module_notification(sender=Module, instance=self.module, created=True)

        # Assertions
        mock_render_to_string.assert_called_once_with('email_new_module.html', {'module': self.module})
        mock_send_mail.assert_called_once_with(
            "New Module Added",
            "Test",
            None,
            ['test@example.com'],
            html_message='<html><body>Test</body></html>'
        )


if __name__ == '__main__':
    unittest.main()

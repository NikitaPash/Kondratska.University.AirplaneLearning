from unittest.mock import patch, Mock

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from discussion_forums.models import Topic, Comment
from discussion_forums.views import send_reply_notification_email
from modules.models import Module, Lesson, Language
from profile_page.models import Profile, LearnerType


class ForumTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.language = Language.objects.create(name='Test Lan', joke='Test Lan')
        self.learner_type = LearnerType.objects.create(title='Test Learner Type')
        self.profile = Profile.objects.create(user=self.user, chosen_language_id=self.language.id,
                                              learner_type_id=self.learner_type.id)
        self.module = Module.objects.create(title='Test Module', language=self.language)
        self.lesson = Lesson.objects.create(title='Test Lesson', module=self.module)
        self.topic = Topic.objects.create(subject=self.lesson, description='Test Desc')

    @patch('discussion_forums.views.send_reply_notification_email')
    def test_add_comment(self, mock_send_reply_notification_email):
        self.client.force_login(self.user)
        data = {
            'comment_text': 'This is a test comment.'
        }
        response = self.client.post(reverse('topic_page', args=[self.topic.id]), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(message='This is a test comment.').exists())
        mock_send_reply_notification_email.assert_called_once()

    @patch('discussion_forums.views.send_mail')
    def test_send_reply_notification_email(self, mock_send_mail):
        comment = Comment.objects.create(
            message='@testuser mentioned you',
            topic=self.topic,
            created_by=self.user.profile,
            created_at=timezone.now()
        )
        comment_text = comment.message
        send_reply_notification_email(comment, comment_text)
        mock_send_mail.assert_called_once()

    @patch('discussion_forums.views.Comment.objects.get')
    def test_delete_comment(self, mock_comment_get):
        mock_comment_instance = Mock()
        mock_comment_get.return_value = mock_comment_instance
        mock_comment_instance.delete.return_value = None

        self.client.force_login(self.user)
        response = self.client.post(reverse('delete_comment', args=[1]))
        self.assertFalse(Comment.objects.filter(id=1).exists())

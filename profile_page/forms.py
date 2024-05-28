from django import forms
from storages.backends.azure_storage import AzureStorage

from ALPP import settings
from .models import Profile, LearnerType


class LearnerTypeSettings(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['learner_type']

    learner_type = forms.ModelChoiceField(queryset=LearnerType.objects.all())


class UsernameSettings(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username']


class ProfilePictureSettings(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic_url']

    def save(self, commit=True):
        instance = super().save(commit=False)
        profile_pic_url = self.cleaned_data.get('profile_pic_url')

        azure_storage = AzureStorage(
            account_name=settings.AZURE_ACCOUNT_NAME,
            account_key=settings.AZURE_ACCOUNT_KEY,
        )

        instance.profile_pic_url = azure_storage.save(profile_pic_url.name, profile_pic_url)

        if commit:
            instance.save()
        return instance


class NotificationSettings(forms.ModelForm):
    receive_notifications = forms.ChoiceField(choices=[('Send', 'Send'), ('Do not send', 'Do not send')])
    new_modules_notifications = forms.ChoiceField(choices=[('Send', 'Send'), ('Do not send', 'Do not send')])
    quiz_results_notifications = forms.ChoiceField(choices=[('Send', 'Send'), ('Do not send', 'Do not send')])
    discussion_notifications = forms.ChoiceField(choices=[('Send', 'Send'), ('Do not send', 'Do not send')])
    new_resources_notifications = forms.ChoiceField(choices=[('Send', 'Send'), ('Do not send', 'Do not send')])

    class Meta:
        model = Profile
        fields = ['receive_notifications', 'new_modules_notifications', 'quiz_results_notifications',
                  'discussion_notifications', 'new_resources_notifications']

    def save(self, commit=True):
        instance = super(NotificationSettings, self).save(commit=False)

        if 'receive_notifications' in self.changed_data:
            if instance.receive_notifications == 'Do not send':
                instance.new_modules_notifications = 'Do not send'
                instance.quiz_results_notifications = 'Do not send'
                instance.discussion_notifications = 'Do not send'
                instance.new_resources_notifications = 'Do not send'
            elif instance.receive_notifications == 'Send':
                instance.new_modules_notifications = 'Send'
                instance.quiz_results_notifications = 'Send'
                instance.discussion_notifications = 'Send'
                instance.new_resources_notifications = 'Send'

        if commit:
            instance.save()

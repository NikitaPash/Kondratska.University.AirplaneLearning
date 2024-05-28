from django import forms

from modules.models import Language
from profile_page.models import Profile, LearnerType


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['chosen_language', 'learner_type']

    learner_type = forms.ModelChoiceField(queryset=LearnerType.objects.all())
    chosen_language = forms.ModelChoiceField(queryset=Language.objects.all())

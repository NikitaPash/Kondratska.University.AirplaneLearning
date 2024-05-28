from django import forms

from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_type', 'description', 'screenshot']

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['feedback_type'].widget.attrs.update({'class': 'form-control sniglet', 'style': 'width:250px'})
        self.fields['description'].widget.attrs.update({'class': 'form-control sniglet', 'rows': '4'})
        self.fields['screenshot'].widget.attrs.update({'class': 'form-control-file', 'accept': 'image/*'})
        self.fields['screenshot'].required = False

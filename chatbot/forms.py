from django import forms
from .models import ChatbotIntent


class UserCreateIntentForm(forms.Form):
    intent = forms.CharField()


class UserCreateSentenceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserCreateSentenceForm, self).__init__(*args, **kwargs)
        self.fields['intent'].initial = ""

    sentence = forms.CharField()
    intent = forms.ModelChoiceField(queryset=ChatbotIntent.objects.all())


class UserCreateResponseForm(forms.Form):
    response = forms.CharField()
    intent = forms.ModelChoiceField(queryset=ChatbotIntent.objects.all())

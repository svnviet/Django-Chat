from django import forms
from .models import ChatbotIntent


class UserCreateIntentForm(forms.Form):
    sentence = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nhập chuỗi các câu phân tách bởi đấu ","'}))
    response = forms.CharField(widget=forms.Textarea())


class UserCreateSentenceForm(forms.Form):
    sentence = forms.CharField()
    intent = forms.ModelChoiceField(queryset=ChatbotIntent.objects.all())

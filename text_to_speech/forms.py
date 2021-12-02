from django import forms

# from django.contrib.auth.models import User

VoiceList = [(1, 'A - Giọng Nữ - Miền Bắc'),
             (2, 'B - Giọng Nam - Miền Bắc'),
             (3, 'C - Giọng Nữ - Miền Bắc'),
             (4, 'D - Giọng Nam - Miền Bắc'),
             (5, 'A - Giọng Nữ - Miền Nam'),
             (6, 'B - Giọng Nam - Miền Nam'),
             (7, 'C - Giọng Nữ - Miền Nam'),
             (8, 'D - Giọng Nam - Miền Nam')]

SpeedList = [(0, 'LOW'), (1, 'TB'), (2, 'QK')]


class TextToSpeechForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TextToSpeechForm, self).__init__(*args, **kwargs)
        self.fields['voice'].label = "Giọng đọc"
        self.fields['speed'].label = "Tốc độ"
        self.fields['content'].label = "Nội dung"

    voice = forms.ChoiceField(choices=VoiceList)
    speed = forms.ChoiceField(choices=SpeedList)
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

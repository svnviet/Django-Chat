from django import forms

# from django.contrib.auth.models import User

VoiceList = [(1, 'Ngọc Hân - Giọng Nữ - Miền Bắc'),
             (2, 'Quang Tuấn - Giọng Nam - Miền Bắc'),
             (3, 'Ngọc Diệp - Giọng Nữ - Miền Bắc'),
             (4, 'Hoàng Anh - Giọng Nam - Miền Bắc'),
             (5, 'Ngọc Linh - Giọng Nữ - Miền Bắc'),
             (6, 'Hoàng Nam - Giọng Nam - Miền Bắc'),
             (7, 'Đặng Loan - Giọng Nữ - Miền Trung'),
             (8, 'Phương Nam - Giọng Nam - Miền Trung')]

SpeedList = [(0.7, '0.25'), (0.8, '0.5'), (0.9, '0.75'), (1, '1'), (1.1, '1.25'), (1.2, '1.5'), (1.3, '1.75')]


class TextToSpeechForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TextToSpeechForm, self).__init__(*args, **kwargs)
        self.fields['voice'].label = "Giọng đọc"
        self.fields['speed'].label = "Tốc độ"
        self.fields['content'].label = "Nội dung"
        self.fields['speed'].initial = "1"

    voice = forms.ChoiceField(choices=VoiceList)
    speed = forms.ChoiceField(choices=SpeedList)
    content = forms.CharField(max_length=500,
                              widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nội dung tối đa 500 kí tự', 'max_length': '500'}))

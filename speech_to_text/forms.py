from django import forms


class SpeechToTextForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SpeechToTextForm, self).__init__(*args, **kwargs)

    audio = forms.FileField(widget=forms.FileInput(attrs={'class': 'audio-input-control', 'onchange': 'call_arc(this)'}))

from django.shortcuts import render
from django.views.generic import FormView
from .forms import SpeechToTextForm
from text_to_speech.models import StoreAudio
from pydub import AudioSegment
from text_to_speech.views import duration_convert, TextToSpeechFormView, speed_change, get_audio_data
from google.cloud import speech
import io
from datetime import datetime
from django.core.files.base import ContentFile
import logging
from django.conf import settings
from django.http import HttpResponseRedirect

# Get an instance of a logger
logger = logging.getLogger(__name__)

language_code = "vi-VN"


# Create your views here.

class SpeechToTextFormView(FormView):
    form_class = SpeechToTextForm
    template_name = "speech_to_text.html"
    success_url = '#'

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect('/login')
        my_form = SpeechToTextForm()
        return render(self.request, self.template_name, {"form": my_form})

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect('/login')
        return self.form_valid(SpeechToTextForm())

    def post(self, request, *args, **kwargs):
        form = SpeechToTextForm()
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect('/login')
        file_obj = self.request.FILES.get('audio')
        name = file_obj.name
        if name[-3:] not in ['wav', 'mp3']:
            error = 'Only support format Wav , Mp3'
        # if name[-3:] == 'mp3':
        #     audio_segment = AudioSegment.from_mp3(self.request.FILES.get('audio'))
        # else:
        audio_segment = AudioSegment(file_obj.file)
        try:
            audio_obj = self.create_audio_object(self.request.user, audio_segment)
            return render(self.request, self.template_name, {"form": form, 'text': audio_obj.text})
        except Exception as e:
            logger.error(str(e))
            error = 'Something went wrong!'
        return render(self.request, self.template_name, {"error": error, "form": form})

    # def convert_mp3_to_wav(self):
    #     file_path = settings.MEDIA_ROOT + f'/tmp/mp3/{datetime.now()}.wav'
    #     import os
    #     if not os.path.exists(settings.MEDIA_ROOT + f'/tmp/mp3'):
    #         os.makedirs(settings.MEDIA_ROOT + f'/tmp/mp3')
    #
    #     audio_segment = AudioSegment.from_mp3(self.request.FILES.get('audio').file)
    #     audio_segment.export(file_path, format='wav')
    #     return get_audio_data(file_path)

    @staticmethod
    def create_audio_object(user_id, audio_segment):
        raw_data = audio_segment.raw_data
        duration_seconds = audio_segment.duration_seconds
        result = speech_to_text(raw_data)
        filename = f"{datetime.now()}.wav"
        audio = ContentFile(raw_data, name=filename)
        new_obj = StoreAudio.objects.create(audio=audio, text=result.get('text'), user_id=user_id,
                                            due_time=duration_seconds,
                                            due_time_display=duration_convert(duration_seconds))
        return new_obj


def speech_to_text(audio):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code=language_code,
    )
    response = client.recognize(config=config, audio=audio)
    try:
        text = response.results[0].alternatives[0].transcript
        confidence = response.results[0].alternatives[0].confidence
    except e:
        return {
            'text': ''
        }
    return {'text': text,
            'confidence': confidence, }

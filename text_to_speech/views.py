from django.shortcuts import render
from django.views.generic import View, CreateView, FormView
from .forms import TextToSpeechForm
from .models import StoreAudio
import google.cloud.texttospeech as tts
from django.core.files.base import ContentFile
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
from cloud_integration.views import UserLoginView
from django.http import HttpResponseRedirect
import mutagen
from pydub import AudioSegment
from django.conf import settings

voice_list = [{'id': 1, 'name': 'A - Giọng Nữ - Miền Bắc', 'code': 'vi-VN-Standard-A', 'gender': 'FEMALE'},
              {'id': 2, 'name': 'B - Giọng Nam - Miền Bắc', 'code': 'vi-VN-Standard-B', 'gender': 'MALE'},
              {'id': 3, 'name': 'C - Giọng Nữ - Miền Bắc', 'code': 'vi-VN-Standard-C', 'gender': 'FEMALE'},
              {'id': 4, 'name': 'D - Giọng Nam - Miền Bắc', 'code': 'vi-VN-Standard-D', 'gender': 'MALE'},
              {'id': 5, 'name': 'A - Giọng Nữ - Miền Nam', 'code': 'vi-VN-Wavenet-A ', 'gender': 'FEMALE'},
              {'id': 6, 'name': 'B - Giọng Nam - Miền Nam', 'code': 'vi-VN-Wavenet-B ', 'gender': 'MALE  '},
              {'id': 7, 'name': 'C - Giọng Nữ - Miền Nam', 'code': 'vi-VN-Wavenet-C ', 'gender': 'FEMALE'},
              {'id': 8, 'name': 'D - Giọng Nam - Miền Nam', 'code': 'vi-VN-Wavenet-D ', 'gender': 'MALE  '}]


class TextToSpeechFormView(FormView):
    form_class = TextToSpeechForm
    template_name = "text_to_speech_form.html"
    success_url = '#'

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect('/login')
        audio_list = StoreAudio.objects.filter(user_id=self.request.user).order_by('-created_at')
        page = self.request.GET.get('page', 1) if self.request.method != 'POST' else 1
        paginator = Paginator(audio_list, 10)
        try:
            audio_list = paginator.page(page)
        except PageNotAnInteger:
            audio_list = paginator.page(1)
        except EmptyPage:
            audio_list = paginator.page(paginator.num_pages)
        if self.request.method == 'POST':
            my_form = TextToSpeechForm(self.request.POST)
            audio_bytes = self.text_to_speech_process(form)
            filename = f"{datetime.now()}.mp3"
            context = form.cleaned_data['content']
            speed = form.cleaned_data['speed']
            if audio_bytes:
                raw_data, due_time = speed_change(audio_bytes, speed)
            else:
                raise ('Exception service')
            audio = ContentFile(raw_data, name=filename)
            new_obj = StoreAudio.objects.create(audio=audio, text=context, user_id=self.request.user, due_time=due_time)
            audio_list = StoreAudio.objects.filter(user_id=self.request.user).order_by('-created_at')
        else:
            my_form = TextToSpeechForm()
            return render(self.request, self.template_name, {"audio_list": audio_list, "form": my_form})
        return render(
            self.request,
            self.template_name,
            {"form": my_form,
             "audio": new_obj.audio,
             "audio_list": audio_list,
             },
        )

    def text_to_speech_process(self, form):
        voice = int(form.cleaned_data['voice'])
        context = form.cleaned_data['content'] + ' .'
        voice_code = [x.get('code').strip() for x in voice_list if x.get('id') == voice]
        return text_to_speech(voice_code[0], context)

    def get(self, request, *args, **kwargs):
        return self.form_valid(False)


def text_to_speech(voice_name: str, text: str):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)
    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )
    return response.audio_content


def speed_change(sound, speed=1):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    # sound = AudioSegment.from_file(self.audio.path)
    source = AudioSegment(sound, sample_width=2, frame_rate=24000 * float(speed), channels=1)
    # source.export()
    return source.raw_data, source.duration_seconds

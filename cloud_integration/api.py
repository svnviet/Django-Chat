from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .api_helper import handle_data_response_success, handle_response_fail, check_permissions
from .models import Customer
from text_to_speech.views import TextToSpeechFormView
from django.http import FileResponse
from text_to_speech.forms import VoiceList
from speech_to_text.views import SpeechToTextFormView
from django.core.files.base import ContentFile
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, FileUploadParser
import requests
import json
from pydub import AudioSegment
from django.conf import settings


# from chatbot.models import ChatBotResponse


class UserTokenGenerate(APIView):
    def post(self, *args, **kwargs):
        data = self.request.data
        uname = data.get('username', '')
        password = data.get("password", '')
        usr = authenticate(username=uname, password=password)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            token = Token.objects.get_or_create(user=usr)
            return Response(handle_data_response_success({'token': token[0].key}), status=HTTP_200_OK)
        return Response(handle_response_fail('username or password not correct'), status=HTTP_200_OK)


class GetVoiceListAvailable(APIView):
    def get(self, *args, **kwargs):
        data = [{'id': vc[0], 'name': vc[1]} for vc in VoiceList]
        return Response(handle_data_response_success(data))


class TextToSpeechRequest(APIView):
    @check_permissions
    def post(self, *args, **kwargs):
        data = self.request.data
        voice_id = data.get('voice')
        text = data.get('text')
        speed = data.get('speed')
        if self.request.content_type != 'application/json':
            return Response(handle_response_fail('Request format is not accept'))
        if not voice_id:
            return Response(handle_response_fail('voice id is not found'))
        if not text:
            return Response(handle_response_fail('text is required'))
        new_obj = TextToSpeechFormView.create_audio_object(self.request.user, voice_id, speed, text)
        response = FileResponse(new_obj.audio.open(), status=200, content_type='audio/wav')
        response.headers['Content-Disposition'] = "inline;filename=sound.wav"
        return response


class SpeechToTextRequest(APIView):
    parser_classes = (FileUploadParser, MultiPartParser, FormParser, JSONParser)

    @check_permissions
    def post(self, *args, **kwargs):
        if self.request.content_type != 'audio/wav':
            return Response(handle_response_fail('Không xác định được định dạng'))

        raw_audio = self.request._request.body

        if not raw_audio:
            return Response(handle_response_fail('Không xác định được định dạng'))

        try:
            audio_segment = AudioSegment(raw_audio)
            audio_size = audio_segment.duration_seconds * audio_segment.frame_width * audio_segment.frame_rate / 1000000
        except Exception as e:
            return Response(handle_response_fail("Không thể phân đoạn định dạng audio!"))

        if audio_segment.duration_seconds > 60 or audio_size > settings.STT_MAX_SIZE:
            return Response(handle_response_fail(f'Chỉ hỗ trợ tệp dưới 1 phút hoặc {settings.STT_MAX_SIZE}Mb!'))
        try:
            audio_obj = SpeechToTextFormView.create_audio_object(self.request.user, audio_segment)
            return Response(handle_data_response_success({'text': audio_obj.text,
                                                          'duration': audio_obj.due_time}))
        except Exception as e:
            logger.error(str(e))
            error = str(e.grpc_status_code.name)
            return Response(handle_response_fail(error))


class SpeechToSpeechRequest(APIView):
    @check_permissions
    def post(self, *args, **kwargs):
        if self.request.content_type != 'audio/wav':
            return Response(handle_response_fail('Request format is not accepted'))
        raw_audio = self.request._request.body
        if not raw_audio:
            return Response(handle_response_fail('Request format is not accept'))
        # stt_obj = SpeechToTextFormView.create_audio_object(self.request.user, raw_audio)
        # intent = self.get_intent_response(stt_obj.text)
        # text_response = self.get_text_response(intent)
        text_response = 'Xin chào ! !'
        if not text_response:
            return Response(handle_response_fail('No Response Exist'))
        tts_obj = TextToSpeechFormView.create_audio_object(self.request.user, 1, 1, text_response)
        response = FileResponse(tts_obj.audio.open(), status=200, content_type='audio/wav')
        response.headers['Content-Disposition'] = "inline;filename=sound.wav"
        return response

    # def get_intent_response(self, text):
    #     url = 'http://0.0.0.0:5005/model/parse'
    #     data = {
    #         'text': text,
    #     }
    #     response = requests.post(url, data=json.dumps(data))
    #     try:
    #         data = response.json()
    #     except:
    #         return Response(handle_response_fail('Something went wrong!'))
    #     intent = data.get('intent')
    #     return intent.get('name')

    # def get_text_response(self, intent):
    #     res_obj = None
    #     if not res_obj:
    #         from chatbot.data.example import create_intent_yaml
    #         return Response(handle_response_fail('No Response exist'))
    #     return res_obj[0].name

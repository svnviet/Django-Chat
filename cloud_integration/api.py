from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .api_helper import handle_data_response_success, handle_response_fail, check_permissions
from .models import Customer
from text_to_speech import views as tts
from django.http import FileResponse
from text_to_speech.forms import VoiceList


class UserTokenGenerate(APIView):
    def post(self, *args, **kwargs):
        data = self.request.data
        uname = data.get('username', '')
        password = data.get("password", '')
        usr = authenticate(username=uname, password=password)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            token = Token.objects.get_or_create(user=usr)
            return Response(handle_data_response_success({'token': token[0].key}), status=HTTP_200_OK)
        return Response(handle_response_fail({'msg': 'username or password not correct'}), status=HTTP_200_OK)


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
            return Response(handle_response_fail({'msg': 'Request format is not accepted'}))
        if not voice_id:
            return Response(handle_response_fail('voice id is not found'))
        if not text:
            return Response(handle_response_fail('text is required'))
        # return
        # audio_bytes = tts.text_to_speech_process(voice_id, text)
        new_obj = tts.TextToSpeechFormView.create_audio_object(kwargs.get('user_id'), voice_id, speed, text)
        response = FileResponse(new_obj.audio.open(), status=200, content_type='audio/wav')
        response.headers['Content-Disposition'] = "inline;filename=sound.wav"
        return response


class SpeechToTextRequest(APIView):
    @check_permissions
    def post(self, *args, **kwargs):
        return Response()

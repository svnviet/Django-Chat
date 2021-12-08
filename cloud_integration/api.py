from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .api_helper import handle_data_response_success, handle_response_fail, check_permissions
from .models import Customer


class UserTokenGenerate(APIView):
    def post(self, *args, **kwargs):
        data = self.request.data
        uname = data.get('username', '')
        password = data.get("password", '')
        usr = authenticate(username=uname, password=password)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            token = Token.objects.get_or_create(user=usr)
            return Response(api_helper.handle_data_response_success({'token': token[0].key}), status=HTTP_200_OK)
        return Response(api_helper.handle_response_fail({'msg': 'username or password not correct'}), status=HTTP_200_OK)


class TextToSpeechRequest(APIView):
    @check_permissions
    def post(self, *args, **kwargs):
        if self.request.content_type != 'application/json':
            return handle_response_fail('Request format is not accepted')
        return Response('ok')

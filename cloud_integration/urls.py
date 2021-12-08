from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from . import api

app_name = 'cloud_integration'
urlpatterns = [
    path('', views.HomePage.as_view(), name='Home'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('register', views.UserRegistrationView.as_view(), name='register'),
    path('logout', views.UserLogoutView.as_view(), name='logout'),
    path(settings.API_EN + 'get-auth-token', api.UserTokenGenerate.as_view(), name='get_auth_token'),
    path(settings.API_EN + 'voice/text/convert', api.TextToSpeechRequest.as_view(), name='speech_to_text'),
    path(settings.API_EN + 'voice', api.GetVoiceListAvailable.as_view(), name='voice')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

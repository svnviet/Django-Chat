from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'text_to_speech'
urlpatterns = [
    path('', views.TextToSpeechFormView.as_view(), name='text'),
    # path(settings.API_EN + 'voice/speech/convert', views.text_to_speech_api(), name="TTS_API"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

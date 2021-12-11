from django.urls import path
from .views import IntentFormView, SentenceFormView, ResponseFormView
from django.conf.urls.static import static
from django.conf import settings

app_name = 'chatbot'
urlpatterns = [
    path('intent', IntentFormView.as_view(), name='intent'),
    path('sentence', SentenceFormView.as_view(), name='sentence'),
    path('response', ResponseFormView.as_view(), name='response'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

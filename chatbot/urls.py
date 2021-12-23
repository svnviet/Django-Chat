from django.urls import path
# from .views import IntentFormView, SentenceFormView, CallFormView, TrainModel, ExampleData
from django.conf.urls.static import static
from django.conf import settings

app_name = 'chatbot'
urlpatterns = [
    # path('intent', IntentFormView.as_view(), name='intent'),
    # path('sentence', SentenceFormView.as_view(), name='sentence'),
    # path('call', CallFormView.as_view(), name='call'),
    # path('training', TrainModel.as_view(), name='training'),
    # path('callbot', CallFormView.chatbot, name='chatbot'),
    # path('create_data', ExampleData.as_view(), name='example_data')
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_CALL)

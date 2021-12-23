from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import View, CreateView, FormView
# from .forms import UserCreateSentenceForm, UserCreateIntentForm
from .models import Sentence, ChatbotIntent
from .model import ChatBot
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response


# Create your views here.


class IntentFormView(FormView):
    form_class = UserCreateIntentForm
    template_name = 'intent_form_view.html'
    success_url = '#'

    def form_valid(self, form):
        if self.request.POST:
            sentences = form.cleaned_data['sentence']
            response = form.cleaned_data['response']
            intent = ChatbotIntent.objects.create(user_id=self.request.user, response=response)
            for sentence in sentences.split(','):
                Sentence.objects.create(intent_id=intent.id, name=sentence)
            form = UserCreateIntentForm()
        intent_list = ChatbotIntent.objects.filter(user_id=self.request.user)
        data = []
        for intent in intent_list:
            data.append({
                'response': intent.response,
                'sentences': [sentence for sentence in Sentence.objects.filter(intent_id=intent.id)]
            })
        return render(self.request, self.template_name, {"intent_list": data, "form": form})

    def get(self, request, *args, **kwargs):
        return self.form_valid(UserCreateIntentForm())


class SentenceFormView(FormView):
    form_class = UserCreateSentenceForm
    template_name = 'sentence_form_view.html'
    success_url = '#'

    def form_valid(self, form):
        if self.request.POST:
            sentence = form.cleaned_data['sentence']
            intent = form.cleaned_data['intent']
            Sentence.objects.create(intent=intent, name=sentence)
            tml_post_request = self.request.POST
            form = UserCreateSentenceForm(tml_post_request)
        sentence_list = Sentence.objects.filter(intent__user_id=self.request.user)
        return render(self.request, self.template_name, {"sentence_list": sentence_list, "form": form})

    def get(self, request, *args, **kwargs):
        return self.form_valid(UserCreateSentenceForm())


class CallFormView(View):
    template_name = 'response_form_view.html'

    def get(self, request, *args, **kwargs):
        return render(self.request, self.template_name, {})

    def post(self, *args, **kwargs):
        return render(self.request, self.template_name, {})

    def chatbot(self, *args, **kwargs):
        bot = ChatBot()
        bot.user_id = self.user
        sentence = 'xin chao'
        res = bot.load_model(sentence)
        return res


class TrainModel(APIView):
    def get(self, request):
        def training_model(user_id):
            data = purpose_nlu_json_data(user_id)
            ChatBot.save_model(ChatBot(), data)

        training_model(self.request.user)
        return Response('ok')


def purpose_nlu_json_data(user_id):
    intent_ids = ChatbotIntent.objects.filter(user_id=user_id)
    sentence_ids = Sentence.objects.filter(intent_id__in=intent_ids)
    data = {}
    nlu = []
    for intent in intent_ids:
        tml_data = {
            'intent': str(intent.id),
            'examples': [sentence.name + '\n' for sentence in sentence_ids if sentence.name]
        }
        nlu.append(tml_data)
    data['nlu'] = nlu
    return data


class ExampleData(APIView):
    def get(self, request):
        import os
        import json
        with open(os.path.join(settings.BASE_DIR, 'chatbot/data/intents.json')) as data:
            data = json.load(data)
            for intent in data['nlu']:
                intent_id = ChatbotIntent.objects.create(response=intent['response'], user_id=self.request.user)
                for sentence in intent['examples'].split('\n'):
                    Sentence.objects.create(intent_id=intent_id.id, name=sentence)
        return Response('ok')

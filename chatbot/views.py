from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import View, CreateView, FormView
from .forms import UserCreateSentenceForm, UserCreateResponseForm, UserCreateIntentForm
from .models import Sentence, ChatBotResponse, ChatbotIntent


# Create your views here.


class IntentFormView(FormView):
    form_class = UserCreateIntentForm
    template_name = 'intent_form_view.html'
    success_url = '#'

    def form_valid(self, form):
        intent = form.cleaned_data['intent']
        ChatbotIntent.objects.create(user_id=self.request.user, name=intent)
        my_form = UserCreateIntentForm()
        intent_list = ChatbotIntent.objects.filter(user_id=self.request.user)
        return render(self.request, self.template_name, {"intent_list": intent_list, "form": my_form})


class SentenceFormView(FormView):
    form_class = UserCreateSentenceForm
    template_name = 'sentence_form_view.html'
    success_url = '#'

    def form_valid(self, form):
        sentence = form.cleaned_data['sentence']
        intent = form.cleaned_data['intent']
        Sentence.objects.create(intent=intent, name=sentence)
        my_form = UserCreateSentenceForm(tml_post_request)
        sentence_list = Sentence.objects.filter(intent__user_id=self.request.user)
        return render(self.request, self.template_name, {"sentence_list": sentence_list, "form": my_form})


class ResponseFormView(FormView):
    form_class = UserCreateResponseForm
    template_name = 'response_form_view.html'
    success_url = '#'

    def form_valid(self, form):
        response = form.cleaned_data['response']
        intent = form.cleaned_data['intent']
        ChatBotResponse.objects.create(intent=intent, name=response)
        my_form = UserCreateResponseForm(self.request.POST)
        response_list = ChatBotResponse.objects.filter(intent__user_id=self.request.user)
        return render(self.request, self.template_name, {"response_list": response_list, "form": my_form})

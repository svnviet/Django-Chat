from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import View, CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, UserLoginForm
from .models import Customer
from rest_framework.authtoken.models import Token


class HomePage(View):
    @staticmethod
    def get(request):
        return redirect("text_to_speech:text")

        # return render(request, 'audio_play.html')


class UserGetToken(View):
    def get(self, request):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect('/login')
        return render(request, 'user_token.html', {'token': Token.objects.filter(user=self.request.user)[0].key})


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = "register.html"
    success_url = reverse_lazy("text_to_speech:text")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("cloud_integration:Home")


class UserLoginView(FormView):
    form_class = UserLoginForm
    template_name = "login.html"
    success_url = reverse_lazy("text_to_speech:text")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        password = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=password)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(
                self.request,
                self.template_name,
                {"form": self.form_class, "error": "Tài khoản không tồn tại"},
            )

        return super().form_valid(form)

from django.shortcuts import render, redirect
# from .models import Film, Showtime, Seat, Booking, Customer
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import View, CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout

from .forms import UserLoginForm


class HomePage(View):
    @staticmethod
    def get(request):
        return render(request, 'audio_play.html')


class UserLoginView(FormView):
    form_class = UserLoginForm
    template_name = "login.html"
    success_url = reverse_lazy("Home")

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

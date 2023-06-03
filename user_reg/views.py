from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from .forms import *
from .models import *


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy(
        'login')  # ленивый редирект, обычный ловит ерор, тк джанго можешт на момент создания класса еще не сгенерить
    # редирект(хз почему)


def check_reg(request):
    if request.user.is_authenticated:
        return render(request, 'base.html')
    else:
        return reverse_lazy('')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('check')

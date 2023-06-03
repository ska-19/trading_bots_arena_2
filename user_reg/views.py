from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from .forms import *
from .models import *

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy(
        'login')  # ленивый редирект, обычный ловит ерор, тк джанго можешт на момент создания класса еще не сгенерить
    # редирект(хз почему)



class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'
    def get_success_url(self):
        return reverse_lazy('home')
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/user/login/')

def profile(request, id):
    if request.user.is_authenticated:
        user = User.objects.get(id=id)
        return render(request, 'profile.html', context={'user': user})
    else:
        return HttpResponseRedirect('/user/login/')

def user_profile(request, id):
    if request.user.is_authenticated:
        user = User.objects.get(id=id)
        return render(request, 'userprofile.html', context={'user': user})
    else:
        return HttpResponseRedirect('/user/login/')

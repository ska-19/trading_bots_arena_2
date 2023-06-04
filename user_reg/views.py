from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from bot.models import Bot

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
        if id == request.user.id:
            context = {
                'user': User.objects.get(id=id),
                'bots':Bot.objects.filter(user_id=id),
            }
            return render(request, 'userprofile.html', context)
        else:
            context = {
                'user': User.objects.get(pk=id),
            }
            # except ObjectDoesNotExist:
            #     messages.warning(request, 'User Does Not Exist')
            # return redirect('home')
            return render(request, 'profile.html', context)
    else:
        return HttpResponseRedirect('/user/login/')


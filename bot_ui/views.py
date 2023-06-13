import random
import string

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView
from .forms import *
from django.shortcuts import render
from bot.models import Bot, Transaction
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from bot.service.bot_service import BotService


class RegisterBot(CreateView):
    form_class = BotCreateForm
    template_name = 'add_bot.html'
    success_url = 'home'

    def form_valid(self, form):
        bots = Bot.objects.filter(user_id=self.request.user.id)
        for bot in bots:
            if bot.bot_name == form.instance.bot_name:
                form.add_error('bot_name', 'Такое имя уже занято')
                return self.form_invalid(form)
        form.instance.base_balance = form.instance.balance
        form.instance.user_id = self.request.user.id
        form.instance.token = ''.join(
            random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for i in range(30))
        response = super().form_valid(form)
        token = str(form.instance.user_id) + "." + str(self.object.pk) + "." + form.instance.token
        context = self.get_context_data(token=token)

        return self.render_to_response(context)


class BotListView(ListView):
    model = Bot
    template_name = 'bots_list.html'
    context_object_name = 'bots'

    def get_queryset(self):
        return Bot.objects.filter(user_id=self.request.user.id)


def load_change_balance(request, pk):
    bot_service = BotService()
    change_balance = bot_service.get_statistic_by_bot(bot_id=pk)
    bot = Bot.objects.get(pk=pk)
    sum_balance = bot.base_balance + change_balance
    data = {
        'change_balance_html': f'{change_balance:.{2}f}',
        'sum_balance_html': f'{sum_balance:.{2}f}'
    }
    return JsonResponse(data)


class BotDetailView(PermissionRequiredMixin, DetailView):
    model = Bot
    template_name = 'bot_detail.html'
    context_object_name = 'bot'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transactions'] = Transaction.objects.filter(bot=self.object)
        return context

    def has_permission(self):
        if self.request.user.is_authenticated and self.request.user.id == self.get_object().user_id:
            return True
        else:
            return False


class AllBotListView(ListView):
    model = Bot
    template_name = 'ranking.html'
    context_object_name = 'bots'

    def get_queryset(self):
        bots = Bot.objects.filter(is_public=True)
        for bot in bots:
            user = User.objects.get(id=bot.user_id)
            bot.user_name = user.username
        return bots


class BotDeleteView(PermissionRequiredMixin, DeleteView):
    model = Bot
    template_name = 'bot_delete.html'
    success_url = reverse_lazy('bots_list')

    def has_permission(self):
        if self.request.user.is_authenticated and self.request.user.id == self.get_object().user_id:
            return True
        else:
            return False


class BotUpdateView(PermissionRequiredMixin, UpdateView):
    model = Bot
    form_class = BotUpdateForm
    template_name = 'bot_update.html'

    def get_success_url(self):
        return reverse_lazy('bot_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        bot = Bot.objects.get(pk=self.kwargs['pk'])
        if bot.bot_name == form.instance.bot_name:
            return super().form_valid(form)
        bots = Bot.objects.filter(user_id=self.request.user.id)
        for bot in bots:
            if bot.bot_name == form.instance.bot_name:
                form.add_error('bot_name', 'Такое имя уже занято')
                return self.form_invalid(form)
        return super().form_valid(form)

    def has_permission(self):
        if self.request.user.is_authenticated and self.request.user.id == self.get_object().user_id:
            return True
        else:
            return False

from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from .forms import BotCreateForm
from django.shortcuts import render
from bot.models import Bot

class RegisterBot(CreateView):
    form_class = BotCreateForm
    template_name = 'add_bot.html'
    success_url = 'home'#просто раномный редирект

    def form_valid(self, form):
        form.instance.base_balance = form.instance.balance
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BotListView(ListView):
    model = Bot
    template_name = 'bots_list.html'
    context_object_name = 'bots'
    def get_queryset(self):
        return Bot.objects.filter(user_id=self.request.user.id)

# 'detail/<int:pk>'
def bot_detail_view(request, pk):
    bot = Bot.objects.get(pk=pk)
    return render(request, 'bot_detail.html', {'bot': bot})





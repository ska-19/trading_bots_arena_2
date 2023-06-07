import random
import string

from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from .forms import BotCreateForm
from django.shortcuts import render
from bot.models import Bot, Transaction


# from bot.service.bot_service import BotService


class RegisterBot(CreateView):
    form_class = BotCreateForm
    template_name = 'add_bot.html'
    success_url = 'home'  # просто раномный редирект

    def form_valid(self, form):
        bots = Bot.objects.filter(user_id=self.request.user.id)
        for bot in bots:
            if bot.bot_name == form.instance.bot_name:
                form.add_error('bot_name', 'Такое имя уже занято')
                return self.form_invalid(form)
        form.instance.base_balance = form.instance.balance
        form.instance.user_id = self.request.user.id
        form.instance.token = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for i in range(30))
        response = super().form_valid(form)
        token = str(form.instance.user_id) + "." + str(self.object.pk) + "." + form.instance.token
        context = self.get_context_data(token=token)

        return self.render_to_response(context)  # типа отрисовка


class BotListView(ListView):
    model = Bot
    template_name = 'bots_list.html'
    context_object_name = 'bots'

    def get_queryset(self):
        return Bot.objects.filter(user_id=self.request.user.id)


def bot_detail_view(request, pk):
    # bot_service = BotService()
    bot = Bot.objects.get(pk=pk)
    transactions = Transaction.objects.filter(bot=bot)
    # закомментированно потому что медленно работает
    change_balance = -63  # bot_service.get_statistic_by_bot(bot_id=pk)
    context = {
        'bot': bot,
        'transactions': transactions,
        'change_balance': change_balance
    }
    return render(request, 'bot_detail.html', context)


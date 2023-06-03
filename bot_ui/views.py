from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from .forms import BotCreateForm


class RegisterBot(CreateView):
    form_class = BotCreateForm
    template_name = 'create_bot.html'
    success_url = 'login'#просто раномный редирект

    def form_valid(self, form):
        form.instance.base_balance = form.instance.balance
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

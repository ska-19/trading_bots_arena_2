from django import forms
from bot.models import Bot


class BotCreateForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ['bot_name', 'balance', 'is_public']


class BotUpdateForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ['bot_name', 'is_public']

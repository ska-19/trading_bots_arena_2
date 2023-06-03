import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import *


class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ("id", "user_id", "bot_name", "token", "base_balance", "balance")


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ("bot_id", "cost", "amount", "token_id", "type")

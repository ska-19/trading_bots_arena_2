from django.db import models


class Bot(models.Model):
    user_id = models.IntegerField()
    bot_name = models.CharField(max_length=255, default='trade_bot')
    token = models.CharField(max_length=255, default='key')
    is_public = models.BooleanField(default=True)
    balance = models.FloatField()
    base_balance = models.FloatField()
    amount_BNBBUSD = models.IntegerField(default=0)
    amount_BTCBUSD = models.IntegerField(default=0)
    amount_ETHBUSD = models.IntegerField(default=0)
    amount_LTCBUSD = models.IntegerField(default=0)
    amount_TRXBUSD = models.IntegerField(default=0)
    amount_XRPBUSD = models.IntegerField(default=0)

    def __str__(self):
        return self.bot_name


class Transaction(models.Model):
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    cost = models.FloatField()
    amount = models.IntegerField()
    token_id = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=255)

from django.db.models import Sum
import asyncio
from bot.models import Bot, Transaction
from bot.util.Parser import Parser


class BotService:
    def __init__(self):
        self.parser = Parser()

    def buy_token(self, token_id, bot_id, amount):
        price = float(self.parser.get_coin_ticker(token_id))
        bot = Bot.objects.get(id=bot_id)
        if self.validate_operation(bot_id=bot_id, price=price, amount=amount, token_id=token_id, type="BUY"):
            updated_data = {"user_id": bot.user_id,
                            "bot_name": bot.bot_name,
                            "token": bot.token,
                            "balance": bot.balance,
                            "base_balance": bot.base_balance,
                            "amount_BNBBUSD": bot.amount_BNBBUSD,
                            "amount_BTCBUSD": bot.amount_BTCBUSD,
                            "amount_ETHBUSD": bot.amount_ETHBUSD,
                            "amount_LTCBUSD": bot.amount_LTCBUSD,
                            "amount_TRXBUSD": bot.amount_TRXBUSD,
                            "amount_XRPBUSD": bot.amount_XRPBUSD}
            updated_data["amount_" + token_id] += amount
            updated_data["balance"] -= float(amount * price)
            bot.__dict__.update(updated_data)
            bot.save()
            transact = Transaction.objects.create(bot_id=bot_id, cost=float(amount * price), amount=float(amount),
                                                  token_id=token_id,
                                                  type="BUY",
                                                  balance=bot.balance,
                                                  amount_BNBBUSD=bot.amount_BNBBUSD,
                                                  amount_BTCBUSD=bot.amount_BTCBUSD,
                                                  amount_ETHBUSD=bot.amount_ETHBUSD,
                                                  amount_LTCBUSD=bot.amount_LTCBUSD,
                                                  amount_TRXBUSD=bot.amount_TRXBUSD,
                                                  amount_XRPBUSD=bot.amount_XRPBUSD)
            return transact

    def sell_token(self, token_id, bot_id, amount):
        price = float(self.parser.get_coin_ticker(token_id))
        bot = Bot.objects.get(id=bot_id)
        if self.validate_operation(bot_id=bot_id, price=price, amount=amount, token_id=token_id, type="SELL"):
            updated_data = {"user_id": bot.user_id,
                            "bot_name": bot.bot_name,
                            "token": bot.token,
                            "balance": bot.balance,
                            "base_balance": bot.base_balance,
                            "amount_BNBBUSD": bot.amount_BNBBUSD,
                            "amount_BTCBUSD": bot.amount_BTCBUSD,
                            "amount_ETHBUSD": bot.amount_ETHBUSD,
                            "amount_LTCBUSD": bot.amount_LTCBUSD,
                            "amount_TRXBUSD": bot.amount_TRXBUSD,
                            "amount_XRPBUSD": bot.amount_XRPBUSD}
            updated_data["amount_" + token_id] -= amount
            updated_data["balance"] += float(amount * price)
            bot.__dict__.update(updated_data)
            bot.save()
            transact = Transaction.objects.create(bot_id=bot_id, cost=float(amount * price), amount=float(amount),
                                                  token_id=token_id,
                                                  type="SELL",
                                                  balance=bot.balance,
                                                  amount_BNBBUSD=bot.amount_BNBBUSD,
                                                  amount_BTCBUSD=bot.amount_BTCBUSD,
                                                  amount_ETHBUSD=bot.amount_ETHBUSD,
                                                  amount_LTCBUSD=bot.amount_LTCBUSD,
                                                  amount_TRXBUSD=bot.amount_TRXBUSD,
                                                  amount_XRPBUSD=bot.amount_XRPBUSD
                                                  )
            return transact

    def coin_ticker(self, token_id):
        return self.parser.get_coin_ticker(token_id)

    def reset_bot(self, bot_id):
        bot = Bot.objects.get(id=bot_id)
        bot.balance = bot.base_balance
        bot.amount_BNBBUSD = 0
        bot.amount_BTCBUSD = 0
        bot.amount_ETHBUSD = 0
        bot.amount_LTCBUSD = 0
        bot.amount_TRXBUSD = 0
        bot.amount_XRPBUSD = 0
        bot.save()
        return bot

    def get_statistic_by_bot(self, bot_id):
        estate = 0.0
        bot = Bot.objects.get(id=bot_id)
        if bot.amount_BNBBUSD != 0:
            estate += float(bot.amount_BNBBUSD) * float(self.parser.get_coin_ticker("BNBBUSD"))
        if bot.amount_BTCBUSD != 0:
            estate += float(bot.amount_BTCBUSD) * float(self.parser.get_coin_ticker("BTCBUSD"))
        if bot.amount_ETHBUSD != 0:
            estate += float(bot.amount_ETHBUSD) * float(self.parser.get_coin_ticker("ETHBUSD"))
        if bot.amount_LTCBUSD != 0:
            estate += float(bot.amount_LTCBUSD) * float(self.parser.get_coin_ticker("LTCBUSD"))
        if bot.amount_TRXBUSD != 0:
            estate += float(bot.amount_TRXBUSD) * float(self.parser.get_coin_ticker("TRXBUSD"))
        if bot.amount_XRPBUSD != 0:
            estate += float(bot.amount_XRPBUSD) * float(self.parser.get_coin_ticker("XRPBUSD"))
        return estate + float(bot.balance) - float(bot.base_balance)

    def get_amount_of_all_coins(self, bot_id):
        bot = Bot.objects.get(id=bot_id)
        wallet = {
            "BNBBUSD": bot.amount_BNBBUSD,
            "BTCBUSD": bot.amount_BTCBUSD,
            "ETHBUSD": bot.amount_ETHBUSD,
            "LTCBUSD": bot.amount_LTCBUSD,
            "TRXBUSD": bot.amount_TRXBUSD,
            "XRPBUSD": bot.amount_XRPBUSD
        }
        return wallet

    def validate_operation(self, bot_id, amount, price, token_id, type):
        if type == "SELL":
            token_amount = Bot.objects.values_list("amount_" + token_id, flat=True).get(id=bot_id)
            return token_amount - amount >= 0
        elif type == "BUY":
            cur_balance = Bot.objects.get(id=bot_id).balance
            return float(price) * amount <= float(cur_balance)

    def check_possession(self, user_id, bot_id):
        return Bot.objects.get(user_id=user_id, id=bot_id) != None

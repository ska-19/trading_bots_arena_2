from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from .models import Bot
from .serializers import BotSerializer, TransactionSerializer
from .service.bot_service import BotService


def encode_token(request):
    a = request.data['token'].split('.')
    request.data["user_id"] = a[0]
    request.data["bot_id"] = a[1]
    request.data["key"] = a[2]
    return request


class BotViewSet(GenericViewSet):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer()
    bot_service = BotService()

    @action(methods=['post'], detail=False)
    def create_bot(self, request):
        request.data["base_balance"] = request.data["balance"]
        serializer = BotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False)
    def get_bots(self, request):
        bots = Bot.objects.filter(user_id=request.data["user_id"])
        return Response({'bots': [
            [{"id": bot.id}, {"bot_name": bot.bot_name}, {"base_balance": bot.base_balance},
             {"current_balance": bot.balance}, {"statistic": self.bot_service.get_statistic_by_bot(bot_id=bot.id)}]
            for bot in bots]})

    @action(methods=['get'], detail=False)
    def get_ticker(self, request):
        return Response({request.data["token_id"]: self.bot_service.coin_ticker(request.data["token_id"])})

    @action(methods=['get'], detail=False)
    def get_bot_wallet(self, request):
        request = encode_token(request)
        bots = Bot.objects.filter(user_id=request.data["user_id"])
        if self.bot_service.check_possession(user_id=request.data["user_id"], bot_id=request.data["bot_id"]):
            return Response({"wallet": self.bot_service.get_amount_of_all_coins(bot_id=request.data["bot_id"])})

    @action(methods=['post'], detail=False)
    def buy(self, request):
        request = encode_token(request)
        if self.bot_service.check_possession(user_id=request.data["user_id"], bot_id=request.data["bot_id"]):
            return Response(TransactionSerializer(
                self.bot_service.buy_token(token_id=request.data["token_id"], bot_id=request.data["bot_id"],
                                           amount=request.data["amount"])).data)

    @action(methods=['post'], detail=False)
    def sell(self, request):
        request = encode_token(request)
        if self.bot_service.check_possession(user_id=request.data["user_id"], bot_id=request.data["bot_id"]):
            return Response(TransactionSerializer(
                self.bot_service.sell_token(token_id=request.data["token_id"], bot_id=request.data["bot_id"],
                                            amount=request.data["amount"])).data)

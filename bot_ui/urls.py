from django.urls import path

from .views import *

urlpatterns = [
    path('', RegisterBot.as_view(), name='add_bot'),
    path('add/', RegisterBot.as_view(), name='add_bot'),
    path('list/', BotListView.as_view(), name='bots_list'),
    path('detail/<int:pk>', BotDetailView.as_view(), name='bot_detail'),
    path('load_Change_Balance/<int:pk>', load_change_balance, name='load_change_balance'),
    path('delete/<int:pk>', BotDeleteView.as_view(), name='bot_delete'),
    path('ranking/', AllBotListView.as_view(), name='ranking'),
    path('update/<int:pk>', BotUpdateView.as_view(), name='bot_edit'),
]
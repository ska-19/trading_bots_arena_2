from django.urls import path

from .views import *

urlpatterns = [
    path('', RegisterBot.as_view(), name='add_bot'),
    path('add/', RegisterBot.as_view(), name='add_bot'),
    path('list/', BotListView.as_view(), name='bots_list'),
    path('detail/<int:pk>', bot_detail_view, name='bot_detail'),

]
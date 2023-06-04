from django.urls import path

from .views import *

urlpatterns = [
    path('', RegisterBot.as_view(), name='add_bot'),
    path('add/', RegisterBot.as_view(), name='add_bot'),
    # path('list/', bots_list, name='bots_list'),
    path('list/', BotListView.as_view(), name='bots_list'),
]
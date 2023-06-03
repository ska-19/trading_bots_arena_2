from django.urls import path

from .views import *

urlpatterns = [
    path('', RegisterBot.as_view(), name='reg'),
]
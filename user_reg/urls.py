from django.urls import path

from .views import *

urlpatterns = [
    path('', RegisterUser.as_view(), name='reg'),
    path('login/',LoginUser.as_view(),name='login'),
    path('check/', check_reg, name='check'),
]
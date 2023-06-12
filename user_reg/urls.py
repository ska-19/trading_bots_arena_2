from django.urls import path

from .views import *

urlpatterns = [
    path('reg/', RegisterUser.as_view(), name='signup'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/<int:id>', profile, name='profile'),
    path('userprofile/<int:id>', user_profile, name='userprofile'),
]

from django.urls import path
from .views import *


urlpatterns = [
    path('zera/users', ZeraUsersView.as_view()),
]
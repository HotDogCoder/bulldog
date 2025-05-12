from django.urls import path
from .views import *


urlpatterns = [
    path('sunat/token', SunatTokenView.as_view()),
    path('mtc/callao/get-callao-car-tickets', CallaoTokenView.as_view()),
]
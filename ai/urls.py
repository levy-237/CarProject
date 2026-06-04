from django.urls import path
from .views import ChatBot

urlpatterns = [
    path("", ChatBot.as_view(), name="chat-bot"),
]
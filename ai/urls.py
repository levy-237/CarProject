from django.urls import path
from .views import ChatBot, Comparator

urlpatterns = [
    path("chat-bot/", ChatBot.as_view(), name="chat-bot"),
    path("compare/", Comparator.as_view(), name="ai-compare"),
]
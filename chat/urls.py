from django.urls import path

from .views import ChatListCreateView, ChatDetailUpdateDeleteView, MessageListCreateView, MessageDetailUpdateDeleteView


urlpatterns = [
    path("chats/", ChatListCreateView.as_view(), name="chat-list"),
    path("chats/<int:pk>/", ChatDetailUpdateDeleteView.as_view(), name="chat-detail"),
    path("messages/", MessageListCreateView.as_view(), name="message-list"),
    path("messages/<int:pk>/", MessageDetailUpdateDeleteView.as_view(), name="message-detail"),


]
from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from config.mixins import UserPermission
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer



class ChatListCreateView(
    # UserPermission,
    generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()

    # disabled for testing
    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_staff:
    #         return Chat.objects.all().order_by("-created_at")

    #     return Chat.objects.filter(Q(sender=user) | Q(recipient=user)).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class ChatDetailUpdateDeleteView(
    # UserPermission,
    generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()
    
    
    # disabled for testing
    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_staff:
    #         return Chat.objects.all()

    #     return Chat.objects.filter(Q(sender=user) | Q(recipient=user))

    def perform_update(self, serializer):
        chat = serializer.instance
        if chat.sender != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You are not the owner of this chat.")

        serializer.save()

    def perform_destroy(self, instance):
        if instance.sender != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You are not the owner of this chat.")

        instance.delete()


class MessageListCreateView(
    # UserPermission,
    generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    
    # disabled for testing
    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_staff:
    #         return Message.objects.all().order_by("created_at")

    #     return Message.objects.filter(
    #         Q(chat__sender=user) | Q(chat__recipient=user)
    #     ).order_by("created_at")

    def perform_create(self, serializer):
        chat = serializer.validated_data.get("chat")
        user = self.request.user

        if chat.sender != user and chat.recipient != user:
            raise PermissionDenied("You are not a member of this chat.")

        serializer.save(sender=user)


class MessageDetailUpdateDeleteView(
    # UserPermission,
    generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    


    # disabled for testing
    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_staff:
    #         return Message.objects.all()

    #     return Message.objects.filter(Q(chat__sender=user) | Q(chat__recipient=user))

    def perform_update(self, serializer):
        message = serializer.instance
        if message.sender != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You are not the owner of this message.")

        chat = serializer.validated_data.get("chat", message.chat)
        if not self.request.user.is_staff and chat.sender != self.request.user and chat.recipient != self.request.user:
            raise PermissionDenied("You are not a member of this chat.")

        serializer.save()

    def perform_destroy(self, instance):
        if instance.sender != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You are not the owner of this message.")

        instance.delete()
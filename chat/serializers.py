from rest_framework import serializers
from .models import Chat, Message

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["id", "created_at", "sender", "recipient", "listing"]
        read_only_fields = ["id", "created_at", "sender"]
        
        
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "created_at", "message", "chat", "sender"]
        read_only_fields = ["id", "created_at", "sender"]
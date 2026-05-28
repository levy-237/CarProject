from rest_framework import serializers
from .models import Chat, Message

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields= ["created_at","sender","recipient","listing"]
        
        
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields= ["created_at","text","chat","sender"]
from channels.db import database_sync_to_async
from .models import Chat, Message
from django.db.models import Q

@database_sync_to_async
def get_chat(chat_id, user):
    try:
        chat = Chat.objects.get(Q(id=chat_id, sender=user) | Q(id=chat_id, recipient=user))
    except Chat.DoesNotExist:
        return None
    return chat

@database_sync_to_async
def create_message(chat, text, sender):
    return Message.objects.create(chat=chat, message=text, sender=sender)
    
    
from django.db import models
from users.models import User
from listings.models import Listing

class ChatManager(models.Manager):
    def get_or_create_chat(self, sender, recipient, listing):
        chat, created = self.get_or_create(
            sender=sender,
            recipient=recipient,
            listing=listing,
        )

        
        return chat

class Chat(models.Model):
    created_at = models.DateField(auto_now_add=True)
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="sent_chats")
    recipient = models.ForeignKey(User,on_delete=models.CASCADE,related_name="received_chats")
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="chats")
    objects = ChatManager()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["sender", "recipient", "listing"],
                name="unique_chat_for_sender_recipient_listing",
            )
        ]

class Message(models.Model):
    created_at = models.DateField(auto_now_add=True)
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE,related_name="messages")
    message = models.TextField(max_length=300)
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="sent_messages")

    
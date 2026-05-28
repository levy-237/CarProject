import json

from channels.generic.websocket import AsyncWebsocketConsumer
from .consumer_helpers import get_chat, create_message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.user = self.scope["user"]
   
        self.chat = await get_chat(self.chat_id,self.user)
        if self.chat is None:
            await self.close(code=4000)
            return
        self.chat_group_name = f"chat_{self.chat.id}"

        # Join room group
        await self.channel_layer.group_add(self.chat_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        
        created_message = await create_message(self.chat, message, self.scope["user"])
        # Send message to room group
        await self.channel_layer.group_send(
            self.chat_group_name, {"type": "chat.message", "message": created_message.message, "created_at": created_message.created_at.isoformat(),"sender": created_message.sender.id}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        created_at = event["created_at"]
        sender = event["sender"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
        "message": message,
        "created_at": created_at,
        "sender": sender,
        }))
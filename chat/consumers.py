
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from .models import Chat, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '').strip()  # strip spaces
        sender = self.scope["user"]

        if not message:
            # Ignore empty or whitespace-only messages
            return

        await self.save_message(sender, self.chat_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
        {
            'type': 'chat_message',
            'message': message,
            'sender': sender.username
        }
    )

    async def chat_message(self, event):
        # This is the handler for 'chat_message' type messages
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
        }))

    @database_sync_to_async 
    def save_message(self, sender, chat_id, message):
        chat = Chat.objects.get(id=chat_id)
        return Message.objects.create(chat=chat, sender=sender, content=message)

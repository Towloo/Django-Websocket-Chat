import json
from datetime import datetime
from asgiref.sync import sync_to_async
from chat.models import Message, Thread
from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.current_user = self.scope["user"]
        username = self.scope["url_route"]["kwargs"]["username"]
        self.user = await sync_to_async(User.objects.get)(username=username)
        self.thread = await sync_to_async(Thread.objects.get_or_create_thread)(self.current_user, self.user)
        self.room_name = f"chat_{self.thread.id}"
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    
    async def disconnect(self, _):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )
    async def receive(self, text_data):
        data = json.loads(text_data)
        mtype = data.get("type")
        if mtype == "message":
            message = data.get("message")
            message = await self.save_message(message)
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type":"chat_message",
                    "message":message.text,
                    "sender":self.current_user.username,
                    "message_id": message.id,
                    "seen": message.seen
                }
            )
        elif mtype == "receipt":
            message = await sync_to_async(Message.objects.prefetch_related('sender').get)(id=data.get("message_id"))
            if not message.seen:
                message.seen = True
                message.read_at = datetime.utcnow()
                await sync_to_async(message.save)()
                await self.channel_layer.group_send(
                    self.room_name,
                    {
                        "type":"chat_message_receipt",
                        "message_id": data.get("message_id"),
                        "sender": message.sender.username
                    }
                )
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message":event.get("message"),
            "sender": event.get("sender"),
            "message_id": event.get("message_id"),
            "type":"message",
            "seen": event.get("seen")
        }))
    
    async def chat_message_receipt(self, event):
        await self.send(text_data=json.dumps({
            "message_id": event.get("message_id"),
            "sender": event.get("sender"),
            "type":"receipt"
        }))

    async def save_message(self, message):
        return await sync_to_async(Message.objects.create)(
            thread=self.thread,
            sender=self.current_user,
            text=message
        )
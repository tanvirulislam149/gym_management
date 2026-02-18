from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print(self.room_name)
        self.private_room = f"chat_room_of_{self.room_name}"
        print(self.private_room)
        await self.channel_layer.group_add(self.private_room, self.channel_name)
        await self.channel_layer.group_add("conversations", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.private_room, self.channel_name)
            await self.channel_layer.group_discard("conversations", self.channel_name)

    async def send_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def send_conversation(self, event):
        print("event convo", event)
        await self.send(text_data=json.dumps({
            "id": event["id"],
            "email": event["email"],
            "first_name": event["first_name"],
            "last_name": event["last_name"]
        }))


class ConversationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print(self.room_name)
        self.private_room = f"conversation_{self.room_name}"
        print(self.private_room)
        await self.channel_layer.group_add(self.private_room, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.private_room, self.channel_name)

    async def send_conversation(self, event):
        print("event convo", event)
        await self.send(text_data=json.dumps({
            "id": event["id"],
            "email": event["email"],
            "image": event["image"],
            "first_name": event["first_name"],
            "last_name": event["last_name"],
            "has_unread": True
        }))



#### New code starts from here -----------------

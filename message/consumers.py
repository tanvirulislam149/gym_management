from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.private_room = f"chat_room_of_{self.room_name}"
        print(self.private_room)
        await self.channel_layer.group_add(self.private_room, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.private_room, self.channel_name)

    async def send_message(self, event):
        print("event", event)
        await self.send(text_data=json.dumps({
            "id": event["id"],
            "message_text": event["message_text"],
            "sender": event["sender"],
            "receiver": event["receiver"],
            "is_read": False
        }))
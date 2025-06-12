from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("public_notification", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard("public_notification", self.channel_name)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'message': event["message"]
        }))
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        author = text_data_json['from']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'from' : author
            }
        )

    async def chatroom_message(self, event):
        message = event['message']
        author = event['from']
        await self.send(text_data=json.dumps({
            'message': message,
            'from' : author
        }))

    pass
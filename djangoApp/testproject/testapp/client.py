import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from .models import Message
from datetime import datetime
User = get_user_model()


class ChatRoomConsumer(AsyncWebsocketConsumer):

    async def fetch(self, data):
        messages = Message.last_10_messages()
        print('Messages:\n')
        print(messages)
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        for message in content['messages']:
           self.send_message(message)
    def messages_to_json(self,messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result
    def message_to_json(self, message):

        return {
            'from': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    def new_message(self,data):
        print('Hello2')
        author = data['from']
        message_ = data['message']
        print(message_)
        print(author)
        user = User.objects.get(username=author)
        print(user.username)

        print('Hello6')
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        message = Message.objects.create(author=user, content=message_)
        message.save()
        print('Hello7')
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)


    async def connect(self):
        print('Hello1')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await (self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    command = {
        'fetch': fetch,
        'new_message': new_message
    }

    async def disconnect(self, close_code):
         await (self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        await self.command[text_data_json['command']](self, text_data_json)

    async def send_message(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        author = text_data_json['from']

        await (self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'from' : author
            }
        )

    async def send_chat_message(self, message):
        print('Hello3')
        Message_dict = message['message']

        message_content = Message_dict['content']
        author = Message_dict['from']
        await(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'content': message_content,
                'from': author,
            }
        )

    async def chat_message(self, event):
        message = event['content']
        author = event['from']
        await self.send(text_data=json.dumps({
            'message': message,
            'from': author
        }))

    pass


import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from .models import Message,Task_model
from datetime import datetime
from .Task import Task
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

    async def new_task(self,data):
        print('Hello')
        task = Task()
        author = data['from']
        print('Hello')
        user = User.objects.get(username=author)
        task_model = Task_model.objects.create(author=user, content_problem=task.task, content_answear=task.answear )
        content = {
                'command': 'new_task',
                'task': self.task_to_json(task_model)
            }
        print('Hello')
        return await self.sendTask(content)
    async def sendTask(self, task):
        print('poka')
        Message_dict = task['task']

        task_content = Message_dict['content_problem']
        task_answear = Message_dict['content_answear']
        author = Message_dict['from']
        print('Hello')
        await (self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_task',
                'content_problem': task_content,
                'content_answear': task_answear,
                'from': author
            }
        )
    def tasks_to_json(self,tasks):
        result = []
        for task in tasks:
            result.append(self.task_to_json(task))
        return result
    def task_to_json(self, task : Task_model):
        return {
            'from': task.author.username,
            'content_problem': task.content_problem,
            'content_answear': task.content_answear,
            'timestamp': str(task.timestamp)
        }
    async def connect(self):
        print('Hello1')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await (self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,

        )

        await self.accept()
    async def check_answear(self, data):
        answear_user = data['message']
        print(answear_user)
        correct_answear = data['answear']

        author = data['from']
        print(str(answear_user) != str(correct_answear))
        if str(answear_user) == str(correct_answear):

            await self.send(text_data=json.dumps({
                'message':  answear_user,
                'from': author,
                'type': 'correct_answear'
            }))
        if str(answear_user) != str(correct_answear):
            print('Here')
            await self.send(text_data=json.dumps({
                    'message': answear_user,
                    'from': author,
                    'type': 'incorrect_answear'
                }))
    command = {
        'fetch': fetch,
        'new_message': new_message,
        'new_task': new_task,
        'check_answear': check_answear
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
    async def send_task(self,event):
        message_problem = event['content_problem']
        message_answear = event['content_answear']
        author = event['from']
        await self.send(text_data=json.dumps({
            'message_problem': message_problem,
            'answear':message_answear,
            'from': author,
            'type': 'problem'
        }))

    async def chat_message(self, event):
        message = event['content']
        author = event['from']
        await self.send(text_data=json.dumps({
            'message': message,
            'from': author
        }))

    pass


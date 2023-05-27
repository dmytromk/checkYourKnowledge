from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from .models import Message,Task_model
from datetime import datetime
from .Task import Task
User = get_user_model()
import json
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    async def execute(self):
        pass

class FetchCommand(Command):
    def __init__(self, consumer, data):
        self.consumer = consumer
        self.data = data

    async def execute(self):
        messages = Message.last_10_messages()
        content = {
            'command': 'messages',
            'messages': self.consumer.messages_to_json(messages)
        }
        for message in content['messages']:
             self.consumer.send_message(message)

class NewMessageCommand(Command):
    def __init__(self, consumer, data):
        self.consumer = consumer
        self.data = data

    async def execute(self):
        print('new message')
        author = self.data['from']
        message_ = self.data['message']
        user = User.objects.get(username=author)
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        message = Message.objects.create(author=user, content=message_)
        message.save()
        content = {
            'command': 'new_message',
            'message': self.consumer.message_to_json(message)
        }
        print(content)
        await self.consumer.send_chat_message(content)

class NewTaskCommand(Command):
    def __init__(self, consumer, data):
        self.consumer = consumer
        self.data = data

    async def execute(self):
        author = self.data['from']
        user = User.objects.get(username=author)
        task = Task()
        task_model = Task_model.objects.create(author=user, content_problem=task.task, content_answear=task.answear)
        content = {
            'command': 'new_task',
            'task': self.consumer.task_to_json(task_model)
        }
        await self.consumer.sendTask(content)


class CheckAnswearCommand(Command):
    def __init__(self, consumer, data):
        self.consumer = consumer
        self.data = data

    async def execute(self):
        answear_user = self.data['message']
        correct_answear = self.data['answear']
        author = self.data['from']

        if str(answear_user) == str(correct_answear):
            await self.consumer.send(text_data=json.dumps({
                'message': answear_user,
                'from': author,
                'type': 'correct_answear'
            }))
        else:
            await self.consumer.send(text_data=json.dumps({
                'message': answear_user,
                'from': author,
                'type': 'incorrect_answear'
            }))


class ChatRoomConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.commands = {
            'fetch': FetchCommand,
            'new_message': NewMessageCommand,
            'new_task': NewTaskCommand,
            'check_answear': CheckAnswearCommand,
        }

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command_name = text_data_json['command']
        command_data = text_data_json
        command_class = self.commands.get(command_name)

        if command_class:
            command : Command = command_class(self, command_data)
            await command.execute()

    def messages_to_json(self,messages : list[json]):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result
    def message_to_json(self, message : json):

        return {
            'from': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    async def sendTask(self, task : json):
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
    def tasks_to_json(self,tasks : list[Task_model]):
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
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await (self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
         await (self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    async def send_message(self, text_data : json):
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

    async def send_chat_message(self, message : Message):
        print('send_chat_message')
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

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from datetime import datetime
from .CommandFactory import *
User = get_user_model()
from .Command import  *

class ChatRoomConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        print('init')
        super().__init__(*args, **kwargs)
        self.listOfTasks = []

    def addTaskToListOfTasks(self,t : Task):
        self.listOfTasks.append(t)

    def getUniqueId(self):
        tasks = Task_model.last_10_tasks()

    def getListOfTasks(self):
        return self.listOfTasks

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command_name = text_data_json['command']
        command_data = text_data_json

        command = CommandFactory.create_command(self, command_name, command_data)
        await command.execute()


    async def sendTask(self, task : json):
        print('poka')
        Message_dict = task['task']

        task_content = Message_dict['content_problem']
        task_answear = Message_dict['content_answer']
        task_name = Message_dict['task_name']
        points = Message_dict['points']
        id = Message_dict['id']
        print('Id:'+str(task_content))
        author = Message_dict['author']
        print('SUCCESS')
        await (self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_task',
                'content_problem': task_content,
                'content_answer': task_answear,
                'author': author,
                'id': id,
                'points': points,
                'task_name': task_name
            }
        )

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
        author = text_data_json['author']

        await (self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'author' : author
            }
        )

    async def send_chat_message(self, message : Message):
        print('send_chat_message')
        Message_dict = message['message']

        message_content = Message_dict['content']
        author = Message_dict['author']
        await(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'content': message_content,
                'author': author,
                 'fetch': False
            }
        )

    async def send_chat_message_fetch(self, message):

        await self.send(text_data=json.dumps(message))
    async def send_Task_model(self, task : Task_model):
        print('send_chat_message')

        task_content = task['content_problem']
        task_answear = task['content_answer']
        author = task['author']
        id = task['id']
        points = task['points']
        task_name = task['task_name']
        print('Hello')
        await (self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_task',
                'content_problem': task_content,
                'content_answer': task_answear,
                'author': author,
                'id': id,
                'points': points,
                'task_name': task_name
            }
        )

    async def send_task(self,event):
        print('send_task')
        message_problem = event['content_problem']
        message_answear = event['content_answer']
        task_name = event['task_name']
        id = event['id']
        print('id' + str(id))
        points = event['points']
        author = event['author']
        await self.send(text_data=json.dumps({
            'type': 'create_task',
            'message_problem': message_problem,
            'answer':message_answear,
            'author': author,

            'id': id,
            'points': points,
            'task_name': task_name
        }))
    async def chat_message(self, event):
        message = event['content']
        author = event['author']
        is_fetch = event['fetch']

        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'content': message,
            'author': author,
            'fetch': is_fetch
        }))

    pass

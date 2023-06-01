from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Message,Task_model
from datetime import datetime
from .Task import Task

User = get_user_model()
import json
from abc import ABC, abstractmethod
from . import JsonConverter

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
        jsonConverter = JsonConverter.JsonConverterContext(JsonConverter.MessageToJsonConverter())
        print(messages)
        content = {
            'command': 'messages',
            'messages': jsonConverter.convert_multiple(messages)
        }

        await self.consumer.send_chat_message_fetch(content)
class FetchTasks(Command):
    def __init__(self, consumer, data):
        self.consumer = consumer
        self.data = data

    async def execute(self):

        class_room = self.data['room_name']
        tasks = Task_model.last_10_tasks(class_room)
        print(len(tasks))
        jsonConverter = JsonConverter.JsonConverterContext(JsonConverter.TaskToJsonConverter())

        content = {
            'command': 'tasks',
            'tasks': jsonConverter.convert_multiple(tasks)
        }
        for task in content['tasks']:
            print(task)
            await self.consumer.sendTask({'task':task})

class GetTask(Command):
    def __init__(self, consumer, data):
        self.consumer = consumer
        self.data = data

    async def execute(self):

        id = self.data['id']
        classroom = self.data['classroom_name']

        tasks = Task_model.objects.all().filter(content_id=id,classroom_name = classroom)
        l : list[json]
        l = []
        for task in tasks:
            l.append({
            'author': task.author.username,
            'content_problem': task.content_problem,
            'content_answer': task.content_answer,
            'id': task.content_id,
            'timestamp': str(task.timestamp),
            'classroom_name': task.classroom_name,
            'points': task.points,
            'task_name': task.task_name
        })
        await self.consumer.sendTask({ 'task' : l[0]})

class NewMessageCommand(Command):
    def __init__(self, consumer, data):
        self.consumer = consumer
        self.data = data

    async def execute(self):
        print('new message')
        author = self.data['author']
        message_ = self.data['message']
        user = User.objects.get(username=author)
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        message = Message.objects.create(author=user, content=message_)
        message.save()
        jsonConverter = JsonConverter.JsonConverterContext(JsonConverter.MessageToJsonConverter())

        content = {
            'command': 'new_message',
            'message': jsonConverter.convert_single(message)
        }
        print(content)
        await self.consumer.send_chat_message(content)

class NewTaskCommand(Command):
    def __init__(self, consumer, data):
        self.consumer = consumer
        self.data = data

    async def execute(self):
        print(self.data)
        author = self.data['author']
        answear = self.data['answer']
        print('NewTaskCommand')
        content = self.data['content']
        classroom = self.data['classroom_name']
        points = self.data['points']
        task_name = self.data['task_name']
        user = User.objects.get(username=author)
        tasks = Task_model.last_10_tasks(classroom)
        print(tasks)
        if(len(tasks)==0):
            id = 1
        else:
            max : int = tasks[0].content_id
            for i in tasks:
                if i.content_id > max:
                    max = i.content_id
            id = 1 + max

        task = Task(content, answear, id,classroom,points,task_name)
        print(id)
        self.consumer.addTaskToListOfTasks(task)
        print(task)
        task_model = Task_model.objects.create(author=user, content_problem=task.task, content_answer=task.answear, content_id=task.id,classroom_name = classroom,points =points,task_name= task.task_name )
        jsonConverter = JsonConverter.JsonConverterContext(JsonConverter.TaskToJsonConverter())

        content = {
            'command': 'new_task',
            'task': jsonConverter.convert_single(task_model)
        }
        await self.consumer.sendTask(content)


class CheckAnswearCommand(Command):
    def __init__(self, consumer, data):
        self.consumer = consumer
        self.data = data

    async def execute(self):
        print(self.data)
        answear_user = self.data['message']
        correct_answear = self.data['answer']
        author = self.data['author']

        print('correct_answer' + correct_answear)
        if str(answear_user) == str(correct_answear):
            await self.consumer.send(text_data=json.dumps({
                'message': answear_user,
                'author': author,
                'type': 'correct_answer'
            }))
        else:
            await self.consumer.send(text_data=json.dumps({
                'message': answear_user,
                'author': author,
                'type': 'incorrect_answer'
            }))


class ChatRoomConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        print('init')
        super().__init__(*args, **kwargs)
        self.commands = {
            'fetch': FetchCommand,
            'new_message': NewMessageCommand,
            'new_task': NewTaskCommand,
            'check_answer': CheckAnswearCommand,
             'get_task' : GetTask,
            'fetch_task': FetchTasks
        }
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
        command_class = self.commands.get(command_name)

        if command_class:
            command : Command = command_class(self, command_data)
            print(command_data)
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
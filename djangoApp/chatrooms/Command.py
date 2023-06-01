from abc import ABC, abstractmethod
from . import JsonConverter
from .models import Message,Task_model
import json
from datetime import datetime
from django.contrib.auth import get_user_model
User = get_user_model()

class Command(ABC):
    @abstractmethod
    async def execute(self):
        pass


class FetchCommand(Command):
    def __init__(self, consumer, data):
        self.consumer = consumer
        self.data = data

    async def execute(self):
        class_room = self.data['room_name']
        messages = Message.last_10_messages(class_room)
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

        await self.consumer.send_chat_message_fetch(content)

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
        classroom = self.data['classroom_name']
        user = User.objects.get(username=author)
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        message = Message.objects.create(author=user, content=message_,classroom_name = classroom)
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

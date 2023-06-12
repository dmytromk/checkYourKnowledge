import json
class ObjectToJsonConverter:
    def convert(self, obj):
        raise NotImplementedError()

class MessageToJsonConverter(ObjectToJsonConverter):
    def convert_single(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp),
            'class_room': message.classroom_name,
            'avatar_link' : message.author.avatar_link,
        }

    def convert_multiple(self, messages: list[json]):
        result = []
        for message in messages:
            result.append(self.convert_single(message))
        return result

class TaskToJsonConverter(ObjectToJsonConverter):

    def convert_single(self, task):

        return {
            'author': task.author.username,
            'content_problem': task.content_problem,
            'content_answer': task.content_answer,
            'timestamp': str(task.timestamp),
            'id': task.content_id,
            'classroom_name': task.classroom_name,
            'points': task.points,
            'task_name': task.task_name
        }

    def convert_multiple(self, tasks: list[json]):
        result = []
        for task in tasks:
            result.append(self.convert_single(task))
        return result


class ClassroomToJson(ObjectToJsonConverter):
    def convert_single(self, classroom):

        return {
            'name': classroom.name,
            'token': classroom.token
        }

    def convert_multiple(self, classrooms):
        result = []
        for classroom in classrooms:
            result.append(self.convert_single(classroom))
        return result

class UserToJson(ObjectToJsonConverter):
    def convert_single(self, user):
        return {
            'name': user.username,
            'avatarLink': user.avatar_link,
            'firstName': user.first_name,
            'lastName': user.last_name,
        }

    def convert_multiple(self, users):
        result = []
        for user in users:
            result.append(self.convert_single(user))
        return result

class AnswerToJson(ObjectToJsonConverter):
    def convert_single(self, answer):

        return {
            'task_id': answer.task_id,
            'author_of_answer': answer.author_of_answer,
            'answer':answer.answer,
            'classroom_token':answer.classroom_token,
            'points':answer.points,
        }

    def convert_multiple(self, anwers):
        result = []
        for answer in anwers:
            result.append(self.convert_single(answer))
        return result

class JsonConverterContext:
    def __init__(self, converter):
        self.converter = converter

    def set_converter(self, converter):
        self.converter = converter

    def convert_single(self, obj):
        return self.converter.convert_single(obj)

    def convert_multiple(self, obj):
        return self.converter.convert_multiple(obj)

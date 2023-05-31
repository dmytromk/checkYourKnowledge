from django.contrib.auth import get_user_model
from django.db import models
from django.utils.crypto import get_random_string
User = get_user_model()


class Message(models.Model):
    author = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    classroom_name = models.TextField()
    def last_10_messages(classroom_name):
        messages = Message.objects.all().filter(classroom_name=classroom_name)
        return messages.order_by('timestamp').all()

class Task_model(models.Model):
    author = models.ForeignKey(User, related_name='tasks',  on_delete=models.CASCADE)
    content_problem = models.TextField()
    content_answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content_id = models.IntegerField()
    classroom_name = models.TextField()
    points = models.IntegerField()
    task_name = models.TextField()
    def last_10_tasks(class_room : str):
        tasks = Task_model.objects.all().filter(classroom_name=class_room)
        return tasks.order_by('timestamp').all()


class Classroom(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    join_code = models.TextField()
    token = models.TextField()

    def generate_invite(self):
        self.join_code = get_random_string(16)
        self.save()
        return self.join_code


class ClassroomUserList(models.Model):
    CLASS_ROLES = [
        ("TE", "teacher"),
        ("ST", "student"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    role = models.TextField(choices=CLASS_ROLES)

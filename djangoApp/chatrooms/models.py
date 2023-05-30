from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()


class Message(models.Model):
    author = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def last_10_messages():
        return Message.objects.order_by('-timestamp').all()[:10]

class Task_model(models.Model):
    author = models.ForeignKey(User, related_name='tasks',  on_delete=models.CASCADE)
    content_problem = models.TextField()
    content_answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content_id = models.IntegerField()
    classroom_name = models.TextField()
    points = models.IntegerField()
    task_name = models.TextField()
    def last_10_tasks(class_room : int):
        tasks = Task_model.objects.all().filter(classroom_name=class_room)
        return tasks.order_by('-timestamp').all()[:10]
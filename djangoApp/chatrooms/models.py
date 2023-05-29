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
    content_answear = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content_id = models.IntegerField()

    def last_10_tasks():
        return Task_model.objects.order_by('-timestamp').all()[:10]
from django.contrib import admin
from .models import Message,Task_model
# Register your models here.
admin.register()
admin.site.register(Message)
admin.site.register(Task_model)
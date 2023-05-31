from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required
from .forms import *

def home(request):
    return render(request, 'home.html', {})


@login_required
def room(request, room_name):
    return render(request, 'chatroom.html', {
        'room_name': room_name,
        'username': mark_safe(json.dumps(request.user.username)),

    })
def createtask(request, room_name):
    return render(request, 'createtask.html', {
        'room_name': room_name,
        'username': mark_safe(json.dumps(request.user.username)),

    })
def task(request, room_name,task_name):
    return render(request, 'task.html', {
        'room_name': room_name,
        'username': mark_safe(json.dumps(request.user.username)),
        'task_name': task_name
    })

# def join_classroom(request, room_code, ):
@login_required()
def create_classroom(request):
    if request.method == 'POST':
        form = ClassroomCreationForm(data=request.POST)
        if form.is_valid():
            classroom = form.save()
            classroom.owner = request.user
            return redirect(f"{classroom.token}")
    else:
        form = ClassroomCreationForm()
    return render(request, 'create_classroom.html',{'form':form})
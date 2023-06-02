from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import Classroom, ClassroomUserList
from . import JsonConverter


def home(request):
    classroomlist = []
    if request.user.is_authenticated:
        classroomlist = [x.classroom for x in ClassroomUserList.objects.filter(user = request.user)]
    jsonConverter = JsonConverter.JsonConverterContext(JsonConverter.ClassroomToJson())
    result = jsonConverter.convert_multiple(classroomlist)
    return render(request, 'home.html', {'classroomlist': result})


@login_required
def room(request, room_name):
    classroom = Classroom.objects.get(token=room_name)
    is_owner = (classroom.owner == request.user)

    return render(request, 'chatroom.html', {
        'room_name': room_name,
        'username': mark_safe(json.dumps(request.user.username)),
        'classroom': classroom,
        'is_owner': is_owner,
    })


def createtask(request, room_name):
    return render(request, 'createtask.html', {
        'room_name': room_name,
        'username': mark_safe(json.dumps(request.user.username)),

    })


def task(request, room_name, task_name):
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
            classroom.save()
            classroom_user = ClassroomUserList()
            classroom_user.classroom = classroom
            classroom_user.user = classroom.owner
            classroom_user.role = "TE"
            classroom_user.save()
            return redirect(f'/chat/{classroom.token}')
    else:
        form = ClassroomCreationForm()
    return render(request, 'create_classroom.html', {'form': form})

@login_required()
def join_class(request):
    if request.method == 'POST':
        form = JoinClassForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            print('LOL')
            if Classroom.objects.filter(join_code=code).exists():
                print('BASED')
                classroom = Classroom.objects.get(join_code=code)
                if ClassroomUserList.objects.filter(classroom=classroom, user=request.user).exists():
                    print('GFSGSDG')
                    user_classroom_token = Classroom.objects.get(join_code=code).token
                    return redirect(f'/chat/{user_classroom_token}')
                else:
                    new_user = ClassroomUserList()
                    new_user.classroom = classroom
                    new_user.role = "ST"
                    new_user.user = request.user
                    new_user.save()
                    return redirect(f'/chat/{classroom.token}')
    else:
        form = JoinClassForm()

    return render(request, 'join_classroom.html', {'form': form})
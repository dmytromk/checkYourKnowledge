from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django import forms
import json
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import Classroom, ClassroomUserList, Answer, Task_model
from . import JsonConverter
from django.contrib.auth import get_user_model
User = get_user_model()


@login_required
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

    users_list = [x.user for x in ClassroomUserList.objects.filter(classroom=classroom)]
    jsonConverter = JsonConverter.JsonConverterContext(JsonConverter.UserToJson())
    users_list = jsonConverter.convert_multiple(users_list)

    classroomlist = [x.classroom for x in ClassroomUserList.objects.filter(user=request.user)] #List of yser`s classrooms
    jsonConverter = JsonConverter.JsonConverterContext(JsonConverter.ClassroomToJson())
    classroomlist = jsonConverter.convert_multiple(classroomlist)


    return render(request, 'chatroom.html', {
        'room_name': room_name,
        'username': mark_safe(json.dumps(request.user.username)),
        'classroom': jsonConverter.convert_single(classroom),
        'is_owner': is_owner,
        'classroomlist': classroomlist,
        'usersList': users_list,
    })


def createtask(request, room_name):
    return render(request, 'createtask.html', {
        'room_name': room_name,
        'username': mark_safe(json.dumps(request.user.username)),

    })


def task(request, room_name, task_name):
    classroom = Classroom.objects.get(token=room_name)
    is_owner = (classroom.owner == request.user)
    return render(request, 'task.html', {
        'room_name': room_name,
        'username': mark_safe(json.dumps(request.user.username)),
        'task_name': task_name,
        'is_owner': is_owner
    })
def user_answer(request, room_name, task_name,student_name):
    return render(request, 'user_answer.html', {
        'room_name': room_name,
        'username': mark_safe(json.dumps(request.user.username)),
        'task_name': task_name,
        'student_name': student_name
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
                form.add_error('code', 'No such classroom. Please enter a valid code.')
    else:
        form = JoinClassForm()

    return render(request, 'join_classroom.html', {'form': form})

@login_required()
def report_generation(request):
    user_id = request.GET.get('user_id')
    classroom_token = request.GET.get('token')
    user = User.objects.get(id=user_id)
    answers = Answer.objects.filter(author_of_answer=user.username, classroom_token=classroom_token)
    tasks = Task_model.objects.filter(classroom_name = classroom_token)

    merged_items = []

    # Merge and iterate over the querysets using zip()
    for task, answer in zip(tasks, answers):
        if task.id == answer.task_id:
            task_id = task.id
            author = task.author.username
            content_problem = task.content_problem
            content_answer = task.content_answer
            content_id = task.content_id
            classroom_name = task.classroom_name
            answer_points = answer.points
            task_name = task.task_name

            # Assign the points attribute directly to max_points
            max_points = task.points

            # Create a dictionary with the merged item
            merged_item = {
                'task_id': task_id,
                'author': author,
                'content_problem': content_problem,
                'content_answer': content_answer,
                'content_id': content_id,
                'classroom_name': classroom_name,
                'answer_points': answer_points,
                'max_points': max_points,
                'task_name': task_name
            }

            # Append the merged item to the list
            merged_items.append(merged_item)

    userToJson = JsonConverter.JsonConverterContext(JsonConverter.UserToJson())
    resultToJson = JsonConverter.JsonConverterContext(JsonConverter.ReportAnswersToJson())

    return render(request, 'report_generation.html', {'answers_list': resultToJson.convert_multiple(merged_items), 'user': userToJson.convert_single(user)})

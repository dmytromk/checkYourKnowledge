from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return  render(request, 'testapp/home.html', {})
@login_required
def room(request, room_name):
    return render(request, 'testapp/chatroom.html', {
        'room_name': room_name,
        'username' : mark_safe(json.dumps(request.user.username)),

    })
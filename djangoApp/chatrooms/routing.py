from django.urls import re_path

from . import client

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', client.ChatRoomConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/createtask/', client.ChatRoomConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/(?P<task_name>\w+)', client.ChatRoomConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/(?P<task_name>\w+)/(?P<student_name>\w+)', client.ChatRoomConsumer.as_asgi())
]
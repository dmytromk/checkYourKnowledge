from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_classroom/', views.create_classroom, name='create_classroom'),
    path('<str:room_name>/', views.room, name='room'),
    path('<str:room_name>/createtask/', views.createtask, name='createtask'),
    path('<str:room_name>/<str:task_name>/', views.task, name='task')
]
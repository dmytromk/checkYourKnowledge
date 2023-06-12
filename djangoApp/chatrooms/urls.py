from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_classroom/', views.create_classroom, name='create_classroom'),
    path('report/', views.report_generation, name='report_generation'),
    path('join_classroom/', views.join_class, name='join_classroom'),
    path('<str:room_name>/', views.room, name='room'),
    path('<str:room_name>/createtask/', views.createtask, name='createtask'),
    path('<str:room_name>/<str:task_name>/', views.task, name='task'),
    path('<str:room_name>/<str:task_name>/<str:student_name>/', views.user_answer, name='user_answer'),
]
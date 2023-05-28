from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
import chatrooms
urlpatterns = [

    path('login/', views.CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logged_out.html'), name='logout'),
    path('registration/', views.register, name='registration'),
    path('change_password/',views.change_password, name='change_password'),
    path('change_email/',views.change_email, name='change_email'),
    path('change_username/',views.change_username, name='change_username'),
    path('settings/',views.settings,name = 'settings'),
]
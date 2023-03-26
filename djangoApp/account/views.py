from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.

class CustomLoginView(LoginView):
    redirect_authenticated_user = True
@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'section': 'dashboard'})
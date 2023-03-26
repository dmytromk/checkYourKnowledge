from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegistrationForm
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.

class CustomLoginView(LoginView):
    redirect_authenticated_user = True

def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            return render(request, 'registration_success.html', {'user': user})
    else:
        user_form = RegistrationForm()
    return render(request, 'registration.html', {'user_form': user_form})


#@login_required
#def dashboard(request):
#    return render(request, 'dashboard.html', {'section': 'dashboard'})
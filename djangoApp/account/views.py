from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordChangeView
from .forms import RegistrationForm, ChangePasswordForm, ChangeEmailForm, ChangeUsernameForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate


# Create your views here.
def home(request):
    return render(request, 'home.html', {})

class CustomLoginView(LoginView):
    redirect_authenticated_user = True

@login_required
def settings(request):
    user = request.user
    # if we make CustomProfile model that extends the built-in django User model then use this instead
    # profile = CustomProfile.objects.get(user=user)
    return render(request, 'settings.html', {'profile': user})

def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            return render(request, 'registration_success.html', {'user': user})
    else:
        user_form = RegistrationForm()
    return render(request, 'registration.html', {'user_form': user_form})

# @login_required()
# def return_data(request):
#     user = get_user_model()
#     return render(request, 'settings.html', {})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user = request.user, data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('/settings')
    else:
        form = ChangePasswordForm(user = request.user)
    return render(request, 'change_password.html', {'form' : form})


@login_required
def change_email(request):
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST, instance=request.user)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=request.user.username, password=password)
            if user is not None:
                user.email = email
                user.save()
                return redirect('/settings')  # Replace with the desired URL or path
            else:
                form.add_error('password', 'Invalid password.')
    else:
        form = ChangeEmailForm(instance=request.user)
    return render(request, 'change_email.html', {'form': form})

@login_required
def change_username(request):
    if request.method == 'POST':
        form = ChangeUsernameForm(request.POST)
        if form.is_valid():
            new_username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=request.user.username, password=password)
            if user is not None:
                user.username = new_username
                user.save()
                return redirect('/settings')  # Replace with the desired URL or path
            else:
                form.add_error('password', 'Invalid password.')
    else:
        form = ChangeUsernameForm(instance=request.user)
    return render(request, 'change_username.html', {'form': form})



#@login_required
#def dashboard(request):
#    return render(request, 'dashboard.html', {'section': 'dashboard'})
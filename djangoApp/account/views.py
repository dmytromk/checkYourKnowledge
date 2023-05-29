from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordChangeView
from .forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate


def home(request):
    return render(request, 'home.html', {})

@login_required
def settings(request):
    return render(request, 'settings.html', {})

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


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user = request.user, data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('/account/settings')
    else:
        form = ChangePasswordForm(user = request.user)
    return render(request, 'change_password.html', {'form' : form})

@login_required
def change_email(request):
    return change_param(request, ChangeEmailForm, 'change_email.html', 'email')

@login_required
def change_username(request):
    return change_param(request,ChangeUsernameForm,'change_username.html','username')

class CustomPasswordResetView(PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'password_reset.html'

def change_param(request,change_function,template_file,attribute):
    if request.method == 'POST':
        form = change_function(request.POST)
        if form.is_valid():
            new_attribute_value = form.cleaned_data[attribute]
            password = form.cleaned_data['password']
            user = authenticate(username=request.user.username, password=password)
            if user is not None:
                setattr(user,attribute,new_attribute_value)
                user.save()
                return redirect('/account/settings')
            else:
                form.add_error('password', 'Invalid password.')
    else:
        form = ChangeUsernameForm(instance=request.user)
    return render(request, 'change_username.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/account/settings')
    else:
        form = ChangePasswordForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})


@login_required
def change_email(request):
    return change_param(request, ChangeEmailForm, 'change_email.html', 'email')


@login_required
def change_username(request):
    return change_param(request, ChangeUsernameForm, 'change_username.html', 'username')


@login_required
def change_realname(request):
    return change_param(request, ChangeRealnameForm, 'change_username.html', 'first_name', 'last_name')


class CustomPasswordResetView(PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'password_reset.html'


def change_param(request, change_function, template_file, *args):
    if request.method == 'POST':
        form = change_function(request.POST)
        if form.is_valid():
            new_attribute_values = []
            for arg in args:
                new_attribute_values.append((arg, form.cleaned_data[arg]))
            password = form.cleaned_data['password']
            user = authenticate(username=request.user.username, password=password)

            if user is not None:
                for attribute_name, attribute_value in new_attribute_values:
                    setattr(user, attribute_name, attribute_value)
                user.save()
                return redirect('/account/settings')
            else:
                form.add_error('password', 'Invalid password.')
    else:
        form = change_function(instance=request.user)
    return render(request, template_file, {'form': form})

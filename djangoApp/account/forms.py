from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm, PasswordResetForm as DjangoPasswordResetForm

from django.contrib.auth.models import User

class BaseCleanedEmailClass:
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

class BaseCleanedUsernameClass:
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

class RegistrationForm(UserCreationForm,BaseCleanedEmailClass,BaseCleanedUsernameClass):
    email = forms.EmailField(required=True)
    model = User
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'})
        }

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ChangePasswordForm(PasswordChangeForm):
    def save(self, commit=True):
        user = self.user
        user.set_password(self.cleaned_data['new_password1'])
        if commit:
            user.save()
        return user

class ChangeEmailForm(forms.ModelForm,BaseCleanedEmailClass):
    email = forms.EmailField(label='New Email', required=True)
    password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']


class ChangeUsernameForm(forms.ModelForm,BaseCleanedUsernameClass):
    username = forms.CharField(label='New Username', max_length=150, required=True)
    password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class PasswordResetForm(DjangoPasswordResetForm):
    email = forms.EmailField(label='Your Email', required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email does not exist.")
        return email


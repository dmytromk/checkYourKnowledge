from django import forms
from .models import Classroom
from django.utils.crypto import get_random_string


class ClassroomCreationForm(forms.ModelForm):
    name = forms.CharField(label="Classroom name")

    class Meta:
        model = Classroom
        fields = ['name']

    def save(self, commit = True):
        classroom = super(ClassroomCreationForm, self).save(commit=False)
        if commit:
            classroom.token = get_random_string(16)
            classroom.save()
        return classroom
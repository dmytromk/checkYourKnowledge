from django import forms
from .models import Classroom
from django.utils.crypto import get_random_string
class ClassroomCreationForm(forms.Form):
    name = forms.CharField(label="Classroom name")

    class Meta:
        model = Classroom
        fields = ['name']

    def save(self, commit = True):
        pass
        # classroom = self.data
        # if commit:
        #
        #     classroom.token = get_random_string(16)
        #     classroom.save()
        # return classroom
from django import forms
from apps.users.models import *

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields=['fname','lname','phone','reg_no','books_due']

class LibmanForm(forms.ModelForm):
    class Meta:
        model = Libman
        fields=['fname','lname','phone','roll_no']
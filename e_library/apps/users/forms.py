from django import forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from .models import *
# noinspection PyUnresolvedReferences
from django.contrib.auth.models import Group


class StudentSignUpForm(UserCreationForm):
    reg_no=forms.CharField(max_length=100)
    phone=forms.CharField(max_length=100)
    books_due=forms.IntegerField(min_value=0)

    class Meta(UserCreationForm.Meta):
        model=User
        fields=('username','first_name','last_name','reg_no','phone','books_due','email','password1','password2')
        labels={'reg_no':'REG NO:'}


    @transaction.atomic
    def save(self):
        user=super().save(commit=False)
        user.email=self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name=self.cleaned_data.get('last_name')
        user.save()
        student = Student.objects.create(user=user)
        profile = user.profile
        profile.email = user.email
        profile.save()
        student.fname=user.first_name
        student.lname = user.last_name
        student.phone=self.cleaned_data.get('phone')
        student.reg_no=self.cleaned_data.get('reg_no')
        student.books_due = self.cleaned_data.get('books_due')
        student.save()
        return user


class LibmanSignUpForm(UserCreationForm):
    roll_no=forms.CharField(max_length=100)
    phone=forms.CharField(max_length=100)
    class Meta(UserCreationForm.Meta):
        model=User
        fields=('username','first_name','last_name','roll_no','phone','email','password1','password2')
        labels={'roll_no':'Roll No:'}


    @transaction.atomic
    def save(self):
        user=super().save(commit=False)
        user.email=self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        libman = Libman.objects.create(user=user)
        profile=user.profile
        profile.email=user.email
        profile.save()
        libman.roll_no = self.cleaned_data.get('roll_no')
        libman.phone=self.cleaned_data.get('phone')
        libman.guest_name=user.first_name
        group = Group.objects.get(name='admin')
        user.groups.add(group)
        libman.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=('image','email','website','biography')


class PasswordResetForm(forms.Form):
    """
    Password reset form
    """
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'required': ''}), min_length=8, max_length=50,
        error_messages={'required': 'Please enter your new password.'})
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'required': ''}), max_length=50,
        error_messages={'required': 'Please re-enter your new password for confirmation.'})

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        if 'password' in self.cleaned_data and self.cleaned_data['password'] != confirm_password:
            raise forms.ValidationError("Your new password and confirm password didn't matched.")
        return confirm_password


class ChangePasswordForm(PasswordResetForm):
    """
    Change password form
    """
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'required': ''}), max_length=50,
        error_messages={'required': 'Please enter your current password.'})
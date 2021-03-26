from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import *
from django.views.generic import CreateView
from .forms import *


def SingUp(request):
    return render(request, 'users/register.html')


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'users/auth/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        try:
            user=form.save()
            login(self.request, user)
            messages.success(self.request, 'User registration success!')
        except:
            messages.error('User registration failure!')
        return redirect('frontpage')


class LibmanSignUpView(CreateView):
    model = User
    form_class = LibmanSignUpForm
    template_name = 'users/auth/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'librarian'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        try:
            user = form.save()
            login(self.request, user)
            messages.success(self.request, 'User registration success!')
        except:
            messages.error('User registration failure!')
        return redirect('frontpage')


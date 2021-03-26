from django.shortcuts import render,redirect
from  django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from apps.books.models import Book
from django.contrib import messages

def home(request):
    book=Book.objects.all()
    paginator = Paginator(book,4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'core/home.html',{'page_obj':page_obj})


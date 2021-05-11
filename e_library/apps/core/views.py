from django.shortcuts import render,redirect
from  django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from apps.books.models import Book
from django.contrib import messages
from django.db.models import Q

def home(request):
    book=Book.objects.all()
    paginator = Paginator(book,4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'core/home.html',{'page_obj':page_obj})



def about(request):
    context ={
        'books_featured': Book.objects.filter(category="Featured"),
        'books_bestseller': Book.objects.filter(category="BestSeller"),
        'books_mostwished': Book.objects.filter(category="MostWished"),
        'books_education': Book.objects.filter(category="Education"),
        'page_name':'about'
    }
    return render(request, 'core/about.html', context)


def simple_book_search(request):
    query = request.GET.get('query', '')
    books = Book.objects.filter(Q(title__icontains=query) | Q(category__icontains=query))

    return render(request, 'core/simple_book_search.html',locals())

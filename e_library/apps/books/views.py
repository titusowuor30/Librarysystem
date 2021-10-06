from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from apps.books.models import Book, Reviews, Borrower
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from apps.users.models import *
from .forms import *
from django.contrib import messages

def search(request):
    book_list = Book.objects.all()
    book_filter = BookFilter(request.GET, queryset=book_list)
    return render(request, 'books/search_book_list.html', {'filter': book_filter})

@login_required
def rate_book(request,pk):
    book=Book.objects.get(pk=pk)
    form = RatingForm()
    if request.method == 'POST':
        form = RatingForm(data=request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book=book
            review.user=request.user
            review.save()
            return redirect('book-detail',pk=review.book.id)
    return render(request, 'books/form.html', locals())

@login_required
def RatingUpdate(request, pk):
    obj =Reviews.objects.get(id=pk)
    form = RatingForm(instance=obj)
    if request.method == 'POST':
        form = RatingForm(data=request.POST, instance=obj)
        if form.is_valid():
           obj = form.save(commit=False)
           obj.save()
           return redirect('book-detail',pk=obj.book.id)
    return render(request, 'books/form.html', locals())


# Book List Displayed
class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'

def show_reviews(request,id):
    book=Book.objects.get(pk=id)
    reviews=book.reviews.all()
    return render(request,'books/book_reviews.html',locals())

# Book Detail Displayed
# class BookDetailView(DetailView):
#     model = Book


@login_required
def BookDetailView(request, pk):
    book = get_object_or_404(Book, id=pk)
    reviews = Reviews.objects.filter(book=book,user=request.user)
    user = request.user
    # stu = Student.objects.get(roll_no=request.user.id)
    rr = Reviews.objects.filter(book=book,user__id=request.user.id)
    print(rr)
    return render(request, 'books/book_detail.html', locals())


# Add a Book
@login_required
def BookCreate(request):
    if not request.user.is_superuser:
        messages.warning(request,"You don have permission to add a book")
        return redirect('frontpage')
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.warning(request,"Book added!")
            return redirect('frontpage')
    return render(request, 'books/book_form.html', locals())

# Update a Book

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'language', 'genre', 'total_copies', 'available_copies', 'category',
              'pic']

    def form_valid(self, form):
        form.instance.lib_author = self.request.user.username
        return super().form_valid(form)



class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = 'book-list/'



def genre_categories(request, genre_slug):
    g = get_object_or_404(Genre, slug=genre_slug)

    return render(request, 'books/genre_categories.html', locals())
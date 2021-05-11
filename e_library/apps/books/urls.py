from django.urls import path
from . import views
from django.conf.urls import url
from django_filters.views import FilterView
from apps.management.filters import BookFilter

urlpatterns = [
    path('book-list/', views.BookListView.as_view(), name='book-list'),
    path('book/<int:pk>/', views.BookDetailView, name='book-detail'),
    path('book/new/', views.BookCreate, name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    url(r'^search/$', FilterView.as_view(filterset_class=BookFilter,
                                         template_name='books/search_book_list.html'), name='search_results'),

    path('rating/update/<int:pk>/', views.RatingUpdate, name='rating_update'),
    path('rating/rate-book/<int:pk>/', views.rate_book, name='rate_book'),
    path('book-reviews/<int:id>/', views.show_reviews, name='book-reviews'),

    path('genre/categories/books<slug:genre_slug>/', views.genre_categories,name='genre_books'),
]

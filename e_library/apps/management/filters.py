from django.contrib.auth.models import User
import django_filters
from apps.books.models import Book
from apps.users.models import Student

class BookFilter(django_filters.FilterSet):
    title=django_filters.CharFilter(lookup_expr='icontains')
    author=django_filters.CharFilter(lookup_expr='icontains')
    genre=django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', ]

class StudentFilter(django_filters.FilterSet):
    name=django_filters.CharFilter(lookup_expr='icontains')
    roll_no=django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Student
        fields = ['name', 'roll_no' ]
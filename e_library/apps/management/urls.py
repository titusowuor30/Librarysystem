from django.urls import path
from . import views

urlpatterns=[
    path('my-books/', views.student_BookListView, name='mybooks'),
    path('book/<int:pk>/request_issue/', views.Borrow, name='borrow'),

]
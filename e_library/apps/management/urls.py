from django.urls import path
from . import views

urlpatterns=[

    path('my-books/<int:student_id>/', views.student_BookListView, name='mybooks'),
    path('book/<int:pk>/request_issue/', views.Borrow, name='borrow'),
    path('return/<int:id>/',views.returnbook, name='return-book'),
    path('student-list/', views.StudentList, name='studentlist'),
    path('student-edit/<int:id>/', views.edit_add_student, name='student-edit'),
    path('student-detail/<int:pk>/',views.StudentDetail,name='student-detail'),
    path('student-book-list/<int:pk>/',views.student_BookListView,name='student_book_list'),
    path('borrower/list/',views.Borrowers,name='borrowers'),
]
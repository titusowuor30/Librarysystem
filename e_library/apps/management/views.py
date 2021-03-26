from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from apps.books.models import *
from apps.users.models import *

#borrow a book
def Borrow(requet,pk):
    bk = Book.objects.get(id=pk)
    stu = Student.objects.get(reg_no=request.user.reg_no)
    stdnt = get_object_or_404(Student, reg_no=str(request.user.reg_no))
    if stdnt.total_books_due < 10:
        message = "Your request to borrow a book has been received!"
        borrower = Borrower()
        borrower.student = stdnt
        borrower.book = bk
        borrower.issue_date = datetime.datetime.now()
        bk.available_copies = bk.available_copies - 1
        bk.save()
        stu.total_books_due = stu.total_books_due + 1
        stu.save()
        borrower.save()
        #return redirect('student_book_list')
    else:
        message = "you have exceeded limit."
    return render(request, 'management/result.html', locals())

#show student book list

@login_required
def student_BookListView(request):
    student=Student.objects.get(reg_no=request.user.reg_no)
    bor=Borrower.objects.filter(student=student)
    book_list=[]
    for b in bor:
        book_list.append(b.book)
    return render(request, 'management/student_book_list.html', locals())
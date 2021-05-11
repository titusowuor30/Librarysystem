from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.books.models import *
from apps.users.models import *
from .forms import *
import datetime


def StudentList(request):
    if request.user.is_superuser:
        students = Student.objects.all()
        return render(request, 'management/student_list.html', {'students': students})

def Borrowers(request):
    bor=Borrower.objects.all()
    return render(request,'management/borrowers.html',locals())

@login_required
def StudentDetail(request, pk):
    student = get_object_or_404(Student, id=pk)
    bor=Borrower.objects.filter(student=student)
    books=Borrower.objects.filter(student=student)
    return render(request, 'management/student_detail.html', locals())


def edit_add_student(request, id=0):
    if request.method == 'GET':
        if id == 0:
            form = StudentForm()
        else:
            student = Student.objects.get(pk=id)
            form = StudentForm(instance=student)
        return render(request, 'users/auth/signup.html', {'form': form})
    else:
        if id == 0:
            form = StudentForm(request.POST)
        else:
            student = Student.objects.get(pk=id)
            form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = student.user
            student.save()
            messages.success(request, 'Student details updated successfully!')
            return redirect('studentlist')


def deletestudent(request, id):
    student = Student.objects.get(pk=id)
    student.delete()
    messages.success('Account has been deleted!')
    return redirect('studentlist')


# borrow a book
@login_required
def Borrow(request, pk):
    bk = get_object_or_404(Book, pk=pk)
    stu = request.user.students
    late_return_charge = Late_return_charge()
    if stu.books_due < 4:
        if bk.available_copies > 2:
            message = "Your request to borrow a book has been received!"
            borrower = Borrower()
            borrower.student = stu
            borrower.book = bk
            borrower.issue_date = datetime.datetime.now()
            borrower.return_date = datetime.date.today() + datetime.timedelta(weeks=3)
            bk.available_copies = bk.available_copies - 1
            bk.save()
            stu.books_due = stu.books_due + 1
            stu.save()
            borrower.save()
            print(borrower)

            # initialize late return charge values
            late_days = 0
            charge = 0.0
            late_return_charge.borrower = borrower
            late_return_charge.late_days = late_days
            late_return_charge.charge = charge
            late_return_charge.save()
        else:
            message = "Remaining copies less than 2,reserved."
    else:
        message = "you have exceeded limit."
    return render(request, 'management/result.html', locals())


# return a book
@login_required
def returnbook(request, id):
    late_return_charge = Late_return_charge()
    if request.user.is_superuser:
        borrower = Borrower.objects.get(pk=id)
        print(borrower)
        book_pk = borrower.book.id
        borrower.student.books_due = student.books_due - 1
        print(borrower.student.books_due)
        student.save()
        book = Book.objects.get(id=book_pk)
        book.available_copies = book.available_copies + 1

        rating = Reviews(review="none", book=book, student=student, rating='2.5')
        rating.save()
        book.available_copies = book.available_copies + 1
        book.save()

        ret_date = borrower.return_date
        date_returned = datetime.date.today()
        days_late = date_returned - ret_date
        charge = 20 * days_late.days
        # update late return charge
        late_return_charge.borrower = borrower
        late_return_charge.late_days = days_late.days
        late_return_charge.charge = charge
        borrower.delete()
        message = "Book has been returned."
    return render(request, 'management/result.html', locals())


# show student book list
@login_required
def student_BookListView(request):
    bor = Borrower.objects.filter(student=request.user.students)
    bor_list = []
    for b in bor:
        bor_list.append(b)
        print(bor)
    return render(request, 'management/student_book_list.html', locals())


def search_student(request):
    student_list = Student.objects.all()
    student_filter = StudentFilter(request.GET, queryset=student_list)
    return render(request, 'management/search_student_list.html', {'filter': student_filter})



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
    try:
        bk = get_object_or_404(Book, pk=pk)
        stu = request.user.students
        late_return_charge = Late_return_charge()
        if stu.books_due < 4:
           if bk.available_copies > 2:
                message = f"Your request to borrow {bk.title} a book has been received!"
                borrower = Borrower()
                borrower.student = stu
                borrower.book = bk
                borrower.issue_date = datetime.date.today()
                borrower.return_date = datetime.date.today() + datetime.timedelta(days=borrower.book.borrowing_duration.duration_allowed)
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
            message = "you have exceeded your borrowing limit."
    except Exception as e:
                message ="\nOnly students registered with the system can borrow books!"    
    return render(request, 'management/result.html', locals())


# return a book
@login_required
def returnbook(request, id):
    late_return_charge = Late_return_charge()
    if request.user.is_superuser:
        book=None
        student=None
        borrower = Borrower.objects.get(pk=id)
        student=borrower.student
        student.books_due = student.books_due - 1
        student.save()
        book = Book.objects.get(id=borrower.book.id)
        book.available_copies = book.available_copies + 1

        rating = Reviews(review="none", book=book, user=request.user, rating='2.5')
        rating.save()
        book.save()

        set_return_date = borrower.return_date
        date_returned = datetime.date.today()
        days_late = date_returned - set_return_date
        print(days_late)
        charge = 20 * days_late.days
        # update late return charge
        late_return_charge.borrower = borrower
        late_return_charge.late_days = days_late.days
        late_return_charge.charge = charge
        late_return_charge.save()
        borrower.delete()
        message = f"The {book.title} Book borrowed by {borrower.student} has been returned."
    return render(request, 'management/result.html', locals())


# show student book list
@login_required
def student_BookListView(request,student_id):
    bor=Borrower.objects.all()
    if request.user.students in bor:
       mybooks=[]
       mybooks.append(bor.book)
       print(mybooks)
    return render(request, 'management/student_book_list.html', locals())


def search_student(request):
    student_list = Student.objects.all()
    student_filter = StudentFilter(request.GET, queryset=student_list)
    return render(request, 'management/search_student_list.html', {'filter': student_filter})



from django.db import models
from apps.users.models import *
from django.shortcuts import reverse
class Status(models.Model):
    title=models.CharField(max_length=100);
    slug=models.SlugField(max_length=255)

    def __str__(self):
        return self.title

#relation containg all genre of books
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")
    slug=models.SlugField(max_length=255)

    def __str__(self):
        return self.name
##  __str__ method is used to override default string returnd by an object


##relation containing language of books
class Language(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        return self.name

#book relation that has 2 foreign key author language
#book relation can contain multiple genre so we have used manytomanyfield
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category=models.CharField(max_length=100,default="Featured",blank=True,null=True,help_text="Featured,MostWished,Education,BestSeller")
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book",related_name='books')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    total_copies = models.IntegerField()
    available_copies = models.IntegerField()
    status=models.ForeignKey(Status,blank=True,null=True,on_delete=models.CASCADE,related_name='books')
    pic=models.ImageField(blank=True, null=True, upload_to='uploads/book_image/%Y%m%d/',default='uploads/users/default.jpg')

    def getImageURL(self):
        if self.pic.url and hasattr(self.pic,'url'):
            return self.pic.url
        else:
            return 'uploads/users/default.jpg'

#return canonical url for an object
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        return self.title


#relation containing info about Borrowed books
#it has  foriegn key book and student for refrencing book nad student
#roll_no is used for identifing students
#if a book is returned than corresponding tuple is deleted from database
class Borrower(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='borrowers')
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name='borrowers')
    issue_date = models.DateTimeField(null=True,blank=True)
    return_date = models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return self.student.fname+" borrowed "+self.book.title




class Reviews(models.Model):
    review=models.CharField(max_length=100,default="none")
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='reviews')
    CHOICES = (
        ('0', '0'),
        ('.5', '.5'),
        ('1', '1'),
        ('1.5', '1.5'),
        ('2', '2'),
        ('2.5', '2.5'),
        ('3', '3'),
        ('3.5', '3.5'),
        ('4', '4'),
        ('4.5', '4.5'),
        ('5', '5'),
    )

    rating=models.CharField(max_length=3, choices=CHOICES, default='1')

    def __str__(self):
        return self.book.title

class Late_return_charge(models.Model):
    borrower=models.ForeignKey(Borrower,related_name='charges',on_delete=models.CASCADE)
    late_days=models.IntegerField(default=0,max_length=100)
    charge=models.DecimalField(max_digits=6,decimal_places=2)

    def __str__(self):
        return f"Charge({self.charge}) for late({self.late_days} days late) return of  \"{self.borrower.book.title}\"  by {self.borrower.student.fname}"
from django import forms
from apps.books.models import *

class RatingForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields=('review','rating')


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields='__all__'
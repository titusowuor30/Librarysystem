from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
path('',views.home,name='frontpage'),
path('about/',views.about, name='about'),
path('simple_book_search/',views.simple_book_search,name='search'),

]
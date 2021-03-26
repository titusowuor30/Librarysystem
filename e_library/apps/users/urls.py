from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
  path('singup/',views.SingUp,name='singup'),
  path('signup/student/', views.StudentSignUpView.as_view(), name='student_signup'),
  path('signup/libman/', views.LibmanSignUpView.as_view(), name='libman_signup'),
  path('login/',auth_views.LoginView.as_view(template_name='users/auth/login.html'),name='login'),
  path('logout/',auth_views.LogoutView.as_view(template_name='users/auth/logout.html'),name='logout'),
]


from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django_filters.views import FilterView
from apps.management.filters import StudentFilter

urlpatterns = [

  path('singup/',views.SingUp,name='singup'),
  path('signup/student/', views.StudentSignUpView.as_view(), name='student_signup'),
  path('signup/libman/', views.LibmanSignUpView.as_view(), name='libman_signup'),
  path('profile/',views.profile, name='profile'),

  path('login/',views.LoginView.as_view(),name='login'),
  path('logout/',auth_views.LogoutView.as_view(template_name='users/auth/logout.html'),name='logout'),

   path('forgot_password/', views.ForgotPasswordView.as_view(), name='accounts_forgot_password'),
   path('change_password/', views.ChangePasswordView.as_view(), name='accounts_change_password'),
   path('password_reset/<int:id>/-<reset_code>/',views.PasswordResetView.as_view(), name='accounts_password_reset'),


    url(r'^search_student/$', FilterView.as_view(filterset_class=StudentFilter,
    template_name='management/search_student_list.html'), name='search_student'),

]


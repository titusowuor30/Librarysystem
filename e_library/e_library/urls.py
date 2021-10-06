"""e_library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from apps.core.views import logOut
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('logout/', logOut, name='logout'),
    # note the override comes before the admin URLs below
    path('admin/logout/', lambda request: redirect('/logout/', permanent=False)),
    path('admin/', admin.site.urls),
    path('',include('apps.core.urls')),
    path('books/',include('apps.books.urls')),
    path('users/',include('apps.users.urls')),
    path('management/',include('apps.management.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns +=staticfiles_urlpatterns()

admin.site.site_header  =  "E-Library Administration"  
admin.site.site_title  =  "E-Library admin site"
admin.site.index_title  =  "E-Library Admin"

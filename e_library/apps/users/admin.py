from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Libman)
admin.site.register(Profile)
admin.site.register(Role)
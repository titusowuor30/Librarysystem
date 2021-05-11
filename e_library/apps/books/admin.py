from django.contrib import admin

from .models import *

admin.site.register(Book)
admin.site.register(Reviews)
admin.site.register(Borrower)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Status)
admin.site.register(Late_return_charge)
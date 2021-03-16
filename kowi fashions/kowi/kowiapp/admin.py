from django.contrib import admin
from django.contrib.auth.models import *
from .models import *
# Register your models here.

admin.site.register(trends)
admin.site.register(feedback)
admin.site.register(CustInfo)
admin.site.register(EmployeeInfo)
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(SubComment)
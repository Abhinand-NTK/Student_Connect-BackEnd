from django.contrib import admin
from .models import CollegeDatabase,Department,Staff,Subject,Student


admin.site.register(CollegeDatabase)
admin.site.register(Department)
admin.site.register(Staff)
admin.site.register(Subject)
admin.site.register(Student)
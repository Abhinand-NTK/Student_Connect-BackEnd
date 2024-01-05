from django.contrib import admin
from .models import CollegeDatabase,Department,Staff,Subject


admin.site.register(CollegeDatabase)
admin.site.register(Department)
admin.site.register(Staff)
admin.site.register(Subject)
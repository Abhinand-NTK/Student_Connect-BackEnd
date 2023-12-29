from django.contrib import admin
from .models import UserAccount,RegisterCollege


class RegisterCollegeAdmin(admin.ModelAdmin):
    list_display = ('collegename', 'state', 'email', 'is_activate','verified')
class SuperAdmin(admin.ModelAdmin):
    list_display = ('email','is_active','is_staff','is_superuser','phone_number')

admin.site.register(RegisterCollege, RegisterCollegeAdmin)
admin.site.register( UserAccount,SuperAdmin)
from django.contrib import admin
from .models import ClassRoom,ClassRoomForTeacher,AttendanInClassroom,ModulesForClassRoomForTeacher

# Register your models here.
admin.site.register(ClassRoom)
admin.site.register(ClassRoomForTeacher)
admin.site.register(AttendanInClassroom)
admin.site.register(ModulesForClassRoomForTeacher)

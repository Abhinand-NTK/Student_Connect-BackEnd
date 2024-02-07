from django.urls import include, path
from rest_framework import routers
from . import views

staffuser  = routers.DefaultRouter()

staffuser.register(r'createclassroom', views.CrudForClassRoom, basename='createclassroom')
staffuser.register(r'getCourses', views.GetCourse, basename='getCourses')
staffuser.register(r'getstudents', views.GetStudents, basename='getstudents')
staffuser.register(r'getclassrooms', views.GetClassRooms, basename='getclassrooms')
staffuser.register(r'getclassroom', views.GetClassRoom, basename='getclassroom')
staffuser.register(r'getprofile', views.StaffUserProfileCrudView, basename='getprofile')
staffuser.register(r'getpro', views.GetPro, basename='getpro')
staffuser.register(r'classforteacher', views.ClassRoomAssignCrudView, basename='classforteacher')
staffuser.register(r'classroomsforteachers', views.GetViewForClassRoomForTeacher, basename='classroomsforteachers')
staffuser.register(r'classroomattendence', views.AttendenceForStudents, basename='classroomattendence')
staffuser.register(r'getclassroomattendence', views.AttendenceForStudents, basename='getclassroomattendence')
staffuser.register(r'createmodulesforclassrooms', views.CrudForModules, basename='createmodulesforclassrooms')
staffuser.register(r'blockclassroom', views.BlcokClass, basename='blockclassroom')


urlpatterns = [
    path('',include(staffuser .urls))
]
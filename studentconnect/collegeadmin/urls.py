
from django.urls import include, path
from rest_framework import routers
from . import views

college_admin  = routers.DefaultRouter()


college_admin .register(r'addcourse', views.CrudCourseView, basename='addcourse')
college_admin .register(r'editcourse', views.CrudCourseView, basename='editcourse')
college_admin .register(r'getallcourse', views.CrudCourseView, basename='getallcourse')

college_admin .register(r'addstaff', views.CrudStaffView, basename='addstaff')
college_admin .register(r'editstaffdetails', views.CrudStaffView, basename='editstaffdetails')
college_admin .register(r'getallstaff', views.CrudStaffView, basename='getallstaff')
college_admin .register(r'blockuser', views.BlockStaff, basename='blockuser')


college_admin .register(r'addsubject', views.CrudSubjectView, basename='addsubject')
college_admin .register(r'editsubject', views.CrudSubjectView, basename='editsubject')
college_admin .register(r'listsubject', views.CrudSubjectView, basename='listsubject')

college_admin .register(r'addsession', views.SessionCrudView, basename='addsession')
college_admin .register(r'editsession', views.SessionCrudView, basename='editsession')
college_admin .register(r'getsession', views.SessionCrudView, basename='listsession')


college_admin .register(r'addstudent', views.StudentCrudView, basename='addstudent')
college_admin .register(r'getstudent', views.StudentCrudView, basename='getstudent')
college_admin .register(r'editstudent', views.StudentCrudView, basename='editstudent')


college_admin .register(r'createAccounforuser', views.CreatingUsersView, basename='createAccounforuser')

college_admin .register(r'existemail', views.ExistEmailsindataBase, basename='existemail')



urlpatterns = [
    path('',include(college_admin .urls))
]

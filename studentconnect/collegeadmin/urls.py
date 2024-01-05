
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


college_admin .register(r'addsubject', views.CrudSubjectView, basename='addsubject')
college_admin .register(r'editsubject', views.CrudSubjectView, basename='editsubject')
college_admin .register(r'listsubject', views.CrudSubjectView, basename='listsubject')

urlpatterns = [
    path('',include(college_admin .urls))
]

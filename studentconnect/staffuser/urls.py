from django.urls import include, path
from rest_framework import routers
from . import views

staffuser  = routers.DefaultRouter()

staffuser.register(r'createclassroom', views.CrudForClassRoom, basename='createclassroom')
staffuser.register(r'getCourses', views.GetCourse, basename='getCourses')
staffuser.register(r'getstudents', views.GetStudents, basename='getstudents')



urlpatterns = [
    path('',include(staffuser .urls))
]
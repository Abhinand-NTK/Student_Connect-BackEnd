from django.urls import include, path
from rest_framework import routers
from . import views

staffuser  = routers.DefaultRouter()

staffuser.register(r'createclassroom', views.CrudForClassRoom, basename='createclassroom')
staffuser.register(r'getCourses', views.GetCourse, basename='getCourses')
staffuser.register(r'getstudents', views.GetStudents, basename='getstudents')
staffuser.register(r'getclassrooms', views.GetClassRooms, basename='getclassrooms')
staffuser.register(r'getclassroom', views.GetClassRoom, basename='getclassroom')


urlpatterns = [
    path('',include(staffuser .urls))
]
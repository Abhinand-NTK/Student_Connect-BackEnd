
from django.urls import include, path
from rest_framework import routers
from . import views

college_admin  = routers.DefaultRouter()
college_admin .register(r'addcourse', views.AddCourseView, basename='addcourse')
college_admin .register(r'editcourse', views.AddCourseView, basename='editcourse')
college_admin .register(r'getallcourse', views.AddCourseView, basename='getallcourse')
urlpatterns = [
    path('',include(college_admin .urls))
]

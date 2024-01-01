
from django.urls import include, path
from rest_framework import routers
from . import views

college_admin  = routers.DefaultRouter()
college_admin .register(r'addcourse', views.AddCourseView, basename='addcourse')
urlpatterns = [
    path('',include(college_admin .urls))
]

from django.urls import include, path
from rest_framework import routers
from . import views

studnet  = routers.DefaultRouter()

studnet.register(r'getsubejcts', views.GetsubjectsToStudent, basename='getsubejcts')
studnet.register(r'media', views.VideosAssignmentForStudent, basename='media')
studnet.register(r'studentattendence', views.StudentAttendence, basename='studentattendence')
studnet.register(r'requestforleave', views.LeaveRequest, basename='requestforleave')

urlpatterns = [
    path('',include(studnet .urls))
]
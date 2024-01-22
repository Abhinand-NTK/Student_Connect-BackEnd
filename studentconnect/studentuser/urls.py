from django.urls import include, path
from rest_framework import routers
from . import views

studnet  = routers.DefaultRouter()

studnet.register(r'getsubejcts', views.GetsubjectsToStudent, basename='getsubejcts')

urlpatterns = [
    path('',include(studnet .urls))
]
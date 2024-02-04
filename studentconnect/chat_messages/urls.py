from django.urls import path,include
from rest_framework import routers
from . import views

messaging  = routers.DefaultRouter()

messaging.register(r'message',views.SendMessageView,'message')
messaging.register(r'connections',views.Connections,'connections')

urlpatterns  = [
    path('',include(messaging.urls))
]


from django.urls import include, path
from rest_framework import routers
from . import views

user = routers.DefaultRouter()
user.register(r'register', views.CollegeRegisterViewSet, basename='register')
user.register(r'register_update', views.CollegeUpdateViewSet, basename='register_update')
user.register(r'list', views.CollegeListViewSet, basename='list')
user.register(r'active_user', views.UserDetails, basename='active_user')
user.register(r'colleges_deatils', views.CollegeDetails, basename='colleges_deatils')
user.register(r'activation_mail', views.Send_Account_Activation_Mail, basename='activation_mail')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.


urlpatterns = [
    path('', include(user.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('test/',views.test,name='test')
]
urlpatterns += user.urls

from django.urls import include, path
from rest_framework import routers
from . import views

blog  = routers.DefaultRouter()

blog.register(r'blogpost', views.BlogPosts, basename='blogpost')
blog.register(r'blogpostlike', views.LikeBlogPost, basename='blogpostlike')
# blog.register(r'blogpostcomment', views.commentBlogPost, basename='blogpostcomment')


urlpatterns = [
    path('',include(blog .urls))
]


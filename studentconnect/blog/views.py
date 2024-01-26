from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import BlogPost
from rest_framework.permissions import IsAuthenticated
from .serializer import SerializerClassFroBlogPostModel

class BlogPost(ModelViewSet):
    """
    Class for creating the Blogpost
    """
    queryset = BlogPost.objects.all()
    serializer_class = SerializerClassFroBlogPostModel
    permission_classes = IsAuthenticated
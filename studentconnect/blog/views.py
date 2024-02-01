from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from collegeadmin.models import Staff, Student
from rest_framework.permissions import IsAuthenticated
from .serializer import SerializerClassFroBlogPostModel, SerializerClassFroBlogPostModelCreate
from rest_framework.response import Response
from rest_framework import status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from channels.db import database_sync_to_async
from .consumers import NotificationConsumer

class BlogPosts(ModelViewSet):
    """
    Class for creating the Blogpost`
    """
    queryset = BlogPost.objects.all()
    serializer_class = SerializerClassFroBlogPostModel
    permisssionclass = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        funtion for creating the instance of the model 
        """
        data = request.data
        try:
            student_instance = Student.objects.get(user_id__id=request.user.id)
            data['author'] = student_instance.student.id
            data['user'] = request.user.id
            data.pop('id')
        except Student.DoesNotExist:
            try:
                student_instance = Staff.objects.get(user_id=request.user.id)
                data['author'] = student_instance.staff.id
                data['user'] = request.user.id
                data.pop('id')
            except Staff.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        post_id = data.get('id')

        if post_id is not None:
            existing_post = BlogPost.objects.get(pk=post_id)
            serializer = SerializerClassFroBlogPostModelCreate(
                existing_post, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)

        serializer = SerializerClassFroBlogPostModelCreate(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
class LikeBlogPost(ModelViewSet):
    """
    Class for like the blog
    """
    queryset = BlogPost.objects.all()
    serializer_class = SerializerClassFroBlogPostModel
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Function for creating a like for the blog post
        """

        
        user = request.user
        blog_id = request.data.get('id')

        if not blog_id:
            return Response({'error': 'Blog post id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            blog = BlogPost.objects.get(id=blog_id)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Blog post does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if blog.likes.filter(user=user).exists():
            # User has already liked the blog post, unlike it
            blog.likes.filter(user=user).delete()
            liked = False
        else:
            # User hasn't liked the blog post, like it
            like = Like.objects.create(user=user)
            blog.likes.add(like)
            liked = True

            author_channel_name = f'user_{blog.user.id}'

            
            self.send_notification_to_user(author_channel_name, f'Your post "{blog.title}" has a new like from {request.user.first_name}.',blog.user.id)


        like_count = blog.likes.count()

        data = BlogPost.objects.all()

        serializer = self.get_serializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def send_notification_to_user(self, channel_name, message, blog_creator_id):
        # Use Django Channels to send the WebSocket notification
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            channel_name,
            {'type': 'send_notification', 'notification': message,'blog_creator_id':blog_creator_id}
        )
   



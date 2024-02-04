from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from .models import *
from collegeadmin.models import Staff, Student
from rest_framework.permissions import IsAuthenticated
from .serializer import SerializerClassFroBlogPostModel, SerializerClassFroBlogPostModelCreate,SerilizerClassForComments
from rest_framework.response import Response
from rest_framework import status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from channels.db import database_sync_to_async
from .consumers import NotificationConsumer
from superadmin.serializer import UserDetailsSerilzer


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
    permission_classes = [IsAuthenticated]

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

            self.send_notification_to_user(
                author_channel_name, f'Your post "{blog.title}" has a new like from {request.user.first_name}.', blog.user.id)

        like_count = blog.likes.count()

        data = BlogPost.objects.all()

        serializer = self.get_serializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def send_notification_to_user(self, channel_name, message, blog_creator_id):
        # Use Django Channels to send the WebSocket notification
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            channel_name,
            {'type': 'send_notification', 'notification': message,
                'blog_creator_id': blog_creator_id}
        )


    
class CommentBlogPost(ModelViewSet):
    """
    Class for handle the comments for a post 
    """
    queryset = Comment.objects.all()
    serializer_class = SerializerClassFroBlogPostModel
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        """
        Post method
        """
        request.data['author'] = request.user
        user = request.user
        blog_id = request.data.get('blogid')
        text = request.data.get('content')

        if not blog_id or not text:
            return Response({'error': 'Blog post id and text are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            blog = BlogPost.objects.get(id=blog_id)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Blog post does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        request.data.pop('blogid')
        comment = Comment.objects.create(**request.data)
        blog.comments.add(comment)

        
        serializer = SerilizerClassForComments(blog.comments, many=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Function for retrieving the comments of a particular post
        """
        blog_id = self.kwargs['pk']
        data = Comment.objects.filter(blogpost=blog_id)
        serializer = SerilizerClassForComments(data, many=True) 
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        """
        Function for delete the instance of the comment model
        """
        # try:
        comment_id = self.kwargs['pk']
        comment_id = self.kwargs['pk']
        comment = Comment.objects.get(id=comment_id)
        blog_id = BlogPost.objects.get(comments=comment)

        comment.delete()

        comments = Comment.objects.filter(blogpost=blog_id.id)
        serializer = SerilizerClassForComments(comments, many=True)
        
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


def get_active_user_data(user_id):
    active_users = UserAccount.objects.filter(id=user_id)
    serializer = UserDetailsSerilzer(active_users, many=True)
    return serializer.data

def notify_active_users(user_data):
    channel_layer = get_channel_layer()
    data = {'type': 'broadcast.active_users', 'data': user_data}
    channel_name = 'active_user_channel'
    async_to_sync(channel_layer.group_send)(channel_name, data)

class ActiveUsersView(viewsets.ReadOnlyModelViewSet):
    """
    Data about the active users
    """
    queryset = UserAccount.objects.all()
    serializer_class = UserDetailsSerilzer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        List of the active users
        """
        # Notify active users to WebSocket consumers
        user_id = request.user.id
        active_user_data = get_active_user_data(user_id)
        notify_active_users(active_user_data)

        return super().list(request, *args, **kwargs)

    
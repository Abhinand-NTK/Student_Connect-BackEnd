from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from collegeadmin.serializer import CrudStaffSerilizer
from collegeadmin.models import Staff,Student
from superadmin.serializer import UserDetailsSerilzer
from .models import *

class SerializerClassFroBlogPostModel(ModelSerializer):
    """
    Serilizer 
    """
    author = CrudStaffSerilizer(read_only=True)
    user_id = serializers.SerializerMethodField()
    user_like_status = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class
        """
        fields = '__all__'
        model  = BlogPost
    def get_user_id(self, obj):
        try:
            staff_instance = Staff.objects.get(staff__id=obj.author.id)
            return staff_instance.user_id.id
        except Staff.DoesNotExist:
            try:
                student_instance = Student.objects.get(student__id=obj.author.id)
                return student_instance.user_id.id
            except Student.DoesNotExist:
                return None  # Handle the case when both Staff and Student instances do not exist
    def get_user_like_status(self, obj):
        user = self.context['request'].user
        # Check if the user has liked the post
        return obj.likes.filter(user=user).exists()


class SerializerClassFroBlogPostModelCreate(ModelSerializer):
    """
    Serilizer 
    """
    class Meta:
        """
        Meta class
        """
        model  = BlogPost
        fields = '__all__'

class SerilizerClassForComments(ModelSerializer):
    """
    Model serializer for comments
    """
    user_commented = UserDetailsSerilzer(source='author', read_only=True)

    class Meta:
        """
        Meta class
        """
        model = Comment
        fields = ['content', 'date_commented', 'id', 'user_commented','author']
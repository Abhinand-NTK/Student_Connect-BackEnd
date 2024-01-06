
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import RegisterCollege, UserAccount


class CollegeDetailsSerilizer(serializers.ModelSerializer):
    """
    Serializer for Get The details of the user.
    """
    class Meta:

        """
        Meta Calss for the getting the collge details.
        """
        model = RegisterCollege
        fields = [
            'collegename', 'state', 'email','id',
            'is_activate', 'verified','Verfication_email_status',
            'user_details'
        ]


class UserDetailsSerilzer(serializers.ModelSerializer):
    """
    Serializer for Get The details of the user.
    """
    class Meta:
        """
        Meta Calss for the getting the Single user details.
        """

        model = UserAccount
        fields = [
            'first_name', 'last_name', 'email', 'is_active',
            'is_superuser', 'user_image', 'phone_number'
        ]


class RegisterCollegeSerilzer(serializers.ModelSerializer):

    """
    Serializer for RegisterCollege model.
    """

    class Meta:
        """
        Meta Calss for the registercollege.
        """
        model = RegisterCollege
        fields = ['collegename', 'state', 'email', 'is_activate', 'verified']
        read_only_fields = ['created', 'verified']



class UpdateCollegeSerializer(serializers.ModelSerializer):

    """
    Serializer class for updating the college details.
    """
    class Meta:
        """
        Meta class for defining the model and fields.
        """
        model = RegisterCollege
        fields = '__all__'



class MyTokenSerilizer(TokenObtainPairSerializer):

    """
     Customising the token.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        print(user.first_name, token)
        token['first_name'] = user.first_name
        token['email'] = user.email
        token['last_name'] = user.last_name
        token['is_active'] = user.is_active
        token['user_type'] = user.user_type
        if user.is_superuser:
            token['is_super_admin'] = user.is_superuser
        else:
            token['is_super_admin'] = False

        return token

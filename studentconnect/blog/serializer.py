from rest_framework.serializers import ModelSerializer
from .models import *

class SerializerClassFroBlogPostModel(ModelSerializer):
    """
    Serilizer 
    """
    class Meta:
        """
        Meta class
        """
        fields = '__all__'
        model  = BlogPost
from rest_framework.serializers import ModelSerializer
from staffuser.models import ClassRoom

class SerializerForGetSubjectsInstudentSide(ModelSerializer):
    """
    Seriliazer
    """
    
    class Meta:
        """
        Class Meta
        """
        fields = '__all__'
        model = ClassRoom
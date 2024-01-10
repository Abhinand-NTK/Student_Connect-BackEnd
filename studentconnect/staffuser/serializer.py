from rest_framework.serializers import ModelSerializer
from .models import ClassRoom
class ClassRoomSerilizer(ModelSerializer):
    """
    class For serilizer  for the manage the classroom
    """
    class Meta:

        model = ClassRoom
        fields = '__all__'  
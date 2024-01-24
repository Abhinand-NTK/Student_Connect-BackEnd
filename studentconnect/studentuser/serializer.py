from rest_framework.serializers import ModelSerializer
from staffuser.models import ClassRoom
from collegeadmin.models import RequestForLeave
from collegeadmin.serializer import CrudStaffSerilizer
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

class SerilizerForLeaveReqeust(ModelSerializer):
    """
    Serilazer Class for the RequestForLeave Modal
    """
    requestor = CrudStaffSerilizer()

    class Meta:
        """
        Meta Class
        """
        model = RequestForLeave
        fields = '__all__'
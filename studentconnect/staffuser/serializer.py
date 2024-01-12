from rest_framework.serializers import ModelSerializer
from .models import ClassRoom
from collegeadmin.serializer import CrudStaffSerilizer,CrudSubjectSerilizer,DepartmentSerializer

class ClassRoomSerilizer(ModelSerializer):
    """
    class For serilizer  for the manage the classroom
    """
    class Meta:

        model = ClassRoom
        fields = '__all__'  

class ClassRoomSerializerWithAllData(ModelSerializer):
    students = CrudStaffSerilizer(many=True, read_only=True)
    staffs_data = CrudStaffSerilizer(many=True, read_only=True)
    subjects = CrudSubjectSerilizer(many=True, read_only=True)
    departments = DepartmentSerializer(many=True,read_only=True)
    class Meta:
       model = ClassRoom
       fields = ['id', 'name', 'students', 'subjects','departments','staffs_data'] 
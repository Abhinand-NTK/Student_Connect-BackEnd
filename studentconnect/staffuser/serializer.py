from rest_framework.serializers import ModelSerializer
from .models import ClassRoom, ClassRoomForTeacher,AttendanInClassroom,ModulesForClassRoomForTeacher
from collegeadmin.models import CollegeDatabase, Staff,Subject,Student
from collegeadmin.serializer import CrudStaffSerilizer, CrudSubjectSerilizer, DepartmentSerializer
from rest_framework import serializers


class ClassRoomSerilizer(ModelSerializer):
    """
    class For serilizer  for the manage the classroom
    """
    class Meta:

        model = ClassRoom
        fields = '__all__'


class ClassRoomSerilizerGet(ModelSerializer):
    """
    class For serilizer  for the manage the classroom
    """
    class Meta:

        model = ClassRoom
        fields = '__all__'
        depth = 4


class ClassRoomSerializerWithAllData(ModelSerializer):
    """"""
    students = CrudStaffSerilizer(many=True, read_only=True)
    staffs_data = CrudStaffSerilizer(many=True, read_only=True)
    subjects = CrudSubjectSerilizer(many=True, read_only=True)
    departments = DepartmentSerializer(many=True, read_only=True)

    class Meta:
        model = ClassRoom
        fields = ['id', 'name', 'students',
                  'subjects', 'departments', 'staffs_data','semester','active']


class StaffUserProfileSerilizer(ModelSerializer):
    """
    class for serilizer the data of the staff model and the related modal
    """

    class Meta:
        """
        Meta class for specify the modal and the fields
        """
        model = Staff
        depth = 2
        fields = '__all__'

class StudentUsersProfileSerilizer(ModelSerializer):
    """
    class for serilizer the data of the staff model and the related modal
    """

    class Meta:
        """
        Meta class for specify the modal and the fields
        """
        model = Student
        depth = 2
        fields = '__all__'


class ClassRoomForTeacherSerializer(ModelSerializer):
    """
    Serializer for the ClassroomForTeacherModal
    """

    def validate(self, data):
        """
        Check if a ClassRoomForTeacher with the same combination of class_id, staff_id, and sub_id already exists
        and if the staff is registered for the given subject.
        """
        class_id = data.get('class_id')
        staff_id = data.get('staff_id')
        sub_id = data.get('sub_id')
        request = self.context.get('request')
        user_id = request.GET.get('id') 
        staff_id=Staff.objects.get(staff_id=user_id)
        # Subject.objects.filter(staff_id = staff_id)

        matching_subjects = Subject.objects.filter(staff_id=staff_id, id=sub_id.id)

        if not matching_subjects.exists():
            raise serializers.ValidationError({'error':"The staff is not registered for this subject."})
        
        existing_instance = ClassRoomForTeacher.objects.filter(
            class_id=class_id, staff_id=staff_id, sub_id=sub_id).first()

        if existing_instance:
            error_message = f"A ClassRoomForTeacher is already register in the name of {staff_id} under the subject {sub_id} ,already exists."
            raise serializers.ValidationError({'error': error_message, 'details': {'existing_instance_id': existing_instance.id}})

        try:
            
            if(sub_id == Subject.objects.get(id=sub_id.id, staff_id=staff_id)):
                subject = Subject.objects.get(id=sub_id.id, staff_id=staff_id)
           
        except Subject.DoesNotExist:
            raise serializers.ValidationError("The staff is not registered for this subject.")

        return data
    class Meta:
        """
        Meta Class
        """
        model = ClassRoomForTeacher
        fields = '__all__'
        
class ClassRoomForTeacherSerializerGet(ModelSerializer):
    """
    Class for getting the request of the teachers in a specific route
    """
    class Meta:
        """
        Class Meta for the above 
        Serilizer
        """
        model = ClassRoomForTeacher
        depth = 4
        fields ='__all__'


class ClassRoomForTeacherSerializers(ModelSerializer):
    """
    Serializer class for the Classroom teachers model
    """
    class Meta:
        """
        Meta Class for the above Model
        """
        model = ClassRoomForTeacher
        depth = 4 
        fields = '__all__'

    def to_representation(self, instance):
        # Use the custom method 'get_extra_data' to include additional data
        representation = super().to_representation(instance)
        extra_data = self.get_extra_data(instance)
        representation.update(extra_data)
        return representation

    def get_extra_data(self, instance):
        # Retrieve the extra data (e.g., students) and format it
        students = instance.class_id.get_students()
        student_data = [{'id': student.id, 'first_name': student.first_name,'last_name': student.last_name} for student in students]

        return {'students': student_data}
    
class SerilizerForAttendenceManagement(ModelSerializer):
    """
    Serializer for serilize the attendence data
    """
    first_name = serializers.CharField(source='student_id.student.first_name', read_only=True)
    last_name = serializers.CharField(source='student_id.student.last_name', read_only=True)
    id = serializers.CharField(source='student_id.student.id', read_only=True)

    class Meta:
        model = AttendanInClassroom
        fields = ['class_room_for_staff_id', 'student_id','id', 'date', 'attendance_status', 'first_name', 'last_name']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Add any additional customization to the representation if needed
        return representation
    
class SerilierClassforModulesForClassRoomForTeacher(ModelSerializer):
    """
    Serilazer for ModulesForClassRoomForTeacher model
    """
    class Meta:
        """
        Meta class
        """
        model = ModulesForClassRoomForTeacher
        fields = '__all__'

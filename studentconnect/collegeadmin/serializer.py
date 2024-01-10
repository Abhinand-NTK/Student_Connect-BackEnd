from rest_framework import serializers
from collegeadmin.models import Department,CollegeDatabase,Subject,Session,Student,Staff

class DataValidationSerilzier(serializers.ModelSerializer):
    """
    Class for Serilize the department 
    """

    class Meta:
        """
        Meta class for valdation among the fields 
        """
        model = None
        fields = '__all__'

        def validate_name(self, value):
            """Custom validation for the name field."""
            if self.instance and self.instance.coursename == value:
                return value  # If updating and the name is not changing, no need for further validation

            if Department.objects.filter(coursename=value, college_name=self.validated_data['college_name']).exists():
                raise serializers.ValidationError('Department with this name already exists in the college')

            if not value.isalpha():
                raise serializers.ValidationError('Invalid Name, Must contain only alphabet characters')

            return value
            
class ListViewSerilzer(serializers.ModelSerializer):
    """
    class for sending the list of the department
    """
    class Meta:
        """
        Meta class for convernt the fields into json for get reqeust 
        """
        model = Department
        fields = ['id',
            'coursename',]
        


class CrudStaffSerilizer(serializers.ModelSerializer):
    """
    class for validating the staff model 
    """
    class Meta:
        """
        Meta class for the validation 
        """
        model = CollegeDatabase
        fields  = '__all__'

class CrudSubjectSerilizer(serializers.ModelSerializer):
    """
    Class for validating the subject model
    """
    class Meta:
        """
        Meta class for validation
        """
        model = Subject
        fields = '__all__'

class SubjectDetailSerializer(serializers.ModelSerializer):
    """
    class for serilize the subject
    """
    staff_name = serializers.CharField(source='staff.staff.first_name', read_only=True)
    course_name = serializers.CharField(source='course.coursename', read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'staff','semseter','staff_name', 'course', 'course_name', 'updated_at', 'created_at']

class CrudSessionSerilzer(serializers.ModelSerializer):
    """
    Class for validating the subject model
    """
    class Meta:
        """
        Meta Calss for valdation
        """
        model = Session
        fields = '__all__'

class StudentCrudSerilizer(serializers.ModelSerializer):
    """
    class for validating the student model
    """

    class Meta:
        model = Student
        fields ='__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    """
    class for validating the department modal
    """
    class Meta:
        model = Department
        fields = '__all__'
            
class StudentWithDetailsSerializer(serializers.ModelSerializer):
    """
    Class for serilize and combine the data for the student complete details
    """
    student_details = CrudStaffSerilizer(source='student', read_only=True)
    course_details = DepartmentSerializer(source='course', read_only=True)
    session_details = CrudSessionSerilzer(source='session', read_only=True)
    class Meta:
        model = Student
        fields = ['course_details', 'session_details', 'student_details','semester']

class StaffWithDetailsSerializer(serializers.ModelSerializer):
    staff_details = CrudStaffSerilizer(source='staff', read_only=True)
    class Meta:
        model = Staff
        fields = ['staff_details','is_hod']
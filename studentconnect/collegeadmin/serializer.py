from rest_framework import serializers
from collegeadmin.models import Department

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
        

       
        
        # def validate_password(self,value):
        #     """Function validation for the password."""
        #     if len(value) < 8:
        #         raise serializers.ValidationError('The Password should be atleast 8 characters')
        #     return value
        # ALLOWED_EMAIL_DOMAINS = ['gmail.com', 'yahoo.com', 'outlook.com', 'example.com']
        # def validate_email(self,value):
        #     """Function validtaging the mail."""
        #     if not any(value.endswith(domain) for domain in self.ALLOWED_EMAIL_DOMAINS):
        #         raise serializers.ValidationError('Invalid email Address ,Must be with valid Domain')
        #     return value
        # def validate_number(self,value):
        #     """Function validatiang the No."""
        #     if not value.isdigit():
        #         raise serializers.ValidationError('Invalid No,The field should have to contain a number')
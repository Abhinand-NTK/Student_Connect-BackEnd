from rest_framework import serializers

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
        ALLOWED_EMAIL_DOMAINS = ['gmail.com', 'yahoo.com', 'outlook.com', 'example.com']

        def validation_name(self,value):
            """Function validation foro the name."""
            if not value.isapha():
                raise serializers.ValidationError('Invalid Name,Must contain Only Alphabetes characters')
            return value
        
        
        
        
        
        
        
        
        
        
        
        # def validate_password(self,value):
        #     """Function validation for the password."""
        #     if len(value) < 8:
        #         raise serializers.ValidationError('The Password should be atleast 8 characters')
        #     return value
        # def validate_email(self,value):
        #     """Function validtaging the mail."""
        #     if not any(value.endswith(domain) for domain in self.ALLOWED_EMAIL_DOMAINS):
        #         raise serializers.ValidationError('Invalid email Address ,Must be with valid Domain')
        #     return value
        # def validate_number(self,value):
        #     """Function validatiang the No."""
        #     if not value.isdigit():
        #         raise serializers.ValidationError('Invalid No,The field should have to contain a number')
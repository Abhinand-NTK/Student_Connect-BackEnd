from superadmin.models import UserAccount
from django.db import models


class CollegeDatabase(models.Model):
    """
    Model for Storing the Student and the staff data
    """

    first_name = models.CharField(max_length=150,blank=False)
    last_name = models.CharField(max_length=150,blank=False)
    user_image = models.ImageField(upload_to='profile',blank=True,null=True)
    age = models.IntegerField(null=False)
    department = models.CharField(max_length=150,null=False)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    zip_code = models.BigIntegerField()
    address = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=20)
    created = models.DateField(blank=False,null=True)
    updated_at = models.DateTimeField(auto_now=True)




class Department(models.Model):
    """
    Model for Creating the department
    """
    """__str__ returns  <type 'str'> """
    
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):  
        
        return self.name

class Subject(models.Model):
    """
    Model for Creating the Subject
    """
    """__str__ returns  <type 'str'> """

    name = models.CharField(max_length=120)
    staff = models.ForeignKey(UserAccount,on_delete=models.CASCADE,)
    course = models.ForeignKey(Department, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Session(models.Model):
    start_year = models.DateField()
    end_year = models.DateField()

    def __str__(self):
        return "From " + str(self.start_year) + " to " + str(self.end_year)

    

class Attendance(models.Model):
    """
    Model for Creating the Attendence
    """
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Staff(models.Model):
    """
    Modal for adding the staff
    """
    staff = models.OneToOneField(CollegeDatabase,on_delete=models.CASCADE)


class Student(models.Model):
    """
    Modal for adding the Studnet 
    """
    staff = models.OneToOneField(CollegeDatabase,on_delete=models.CASCADE)
    session = models.ForeignKey(Session,on_delete=models.CASCADE)
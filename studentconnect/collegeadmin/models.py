from superadmin.models import UserAccount
from django.db import models
from superadmin.models import RegisterCollege,UserAccount



class CollegeDatabase(models.Model):
    """
    Model for Storing the Student and the staff data    
    
    """
    
    collge_id = models.ForeignKey(RegisterCollege,on_delete=models.CASCADE,null=True)
    email = models.CharField(max_length=150,blank=True,null=True)
    first_name = models.CharField(max_length=150,blank=True,null=True)
    last_name = models.CharField(max_length=150,blank=True,null=True)
    user_image = models.ImageField(upload_to='profile',blank=True,null=True)
    age = models.IntegerField(null=True)
    city = models.CharField(max_length=150 ,null=True)
    state = models.CharField(max_length=150,null=True)
    zip_code = models.BigIntegerField(null=True)
    address = models.CharField(max_length=300,null=True,blank=True)
    phone_number = models.CharField(max_length=20,null=True)
    primary_password = models.CharField(max_length=150,blank=True,null=True)
    email_sent = models.BooleanField(default=False,null=True)
    created = models.DateField(blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Department(models.Model):
    """
    Model for Creating the department
    """
    """__str__ returns  <type 'str'> """
    
    coursename = models.CharField(max_length=120)
    college_name = models.ForeignKey(RegisterCollege,on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False,null=True)

    def __str__(self):  
        
        return self.coursename

class Staff(models.Model):
    """
    Modal for adding the staff
    """
    user_id = models.ForeignKey(UserAccount,on_delete=models.CASCADE,null=True)
    staff = models.OneToOneField(CollegeDatabase,on_delete=models.CASCADE)
    is_hod = models.BooleanField(null=True,blank=True,default=False)

    def __str__(self):
        return f"{self.staff.first_name} {self.staff.last_name}"

class Subject(models.Model):
    """
    Model for Creating the Subject
    """
    """__str__ returns  <type 'str'> """

    name = models.CharField(max_length=120)
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE,)
    semseter = models.IntegerField(null=True)
    course = models.ForeignKey(Department, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True,null=True)

    def __str__(self):
        return self.name


class Session(models.Model):
    """
    Class for adding the session in the college
    """
    college_id = models.ForeignKey(RegisterCollege,on_delete=models.CASCADE,null=True)
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



class Student(models.Model):
    """
    Modal for adding the Studnet 
    """
    user_id = models.ForeignKey(UserAccount,on_delete=models.CASCADE,null=True)
    student = models.OneToOneField(CollegeDatabase,on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    session = models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    semester = models.CharField(null=True,blank=True)
    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name}"


class RequestForLeave(models.Model):
    """
    Class for reqeusting leave 
    """
    requestor = models.ForeignKey(CollegeDatabase,on_delete=models.CASCADE)
    reasonforleave = models.CharField(max_length=300,null=True)
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    leavetype = models.CharField(null=True)
    approval_status = models.BooleanField(null=True,default=False)

    def __str__(self) -> str:
        """Str funtion for returing a obejct of the class"""
        return f"{self.requestor.first_name}{self.approval_status}"

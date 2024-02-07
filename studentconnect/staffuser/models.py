from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from superadmin.models import RegisterCollege
from collegeadmin.models import Department,Staff,Subject,Student,CollegeDatabase

# Create your models here.

class ClassRoom(models.Model):
    """
    class for adding the classroom
    """
    college_id = models.ForeignKey(RegisterCollege,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length = 150,null=True)
    course = models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    semester = models.CharField(max_length=20,null=True)
    active = models.BooleanField(default=True,null=True)

    students_ids = models.CharField(
        max_length=255,
        validators=[validate_comma_separated_integer_list],
        blank=True,
        null=True
    )


    subject_ids = models.CharField(
        max_length=255,
        validators=[validate_comma_separated_integer_list],
        blank=True,
        null=True
    )

    def set_students_array(self, integers):
        """
        For storing the students id_s into a string format
        """
        self.students_ids = ','.join(map(str, integers))

    def get_students_array(self):
        """
        Get the students that is saved in the object
        """
        return list(map(int, filter(None, self.students_ids.split(','))))

    def set_subjects_array(self, integers):
        """
        For storing the subjects id_s into a string format

        """
        self.subject_ids = ','.join(map(str, integers))

    def get_subjects_array(self):
        """
        Function for getting the array of the subjects in the classroom
        """
        return list(map(int, filter(None, self.subject_ids.split(','))))
    
    def get_subjects(self):
        """
        Returns a queryset of subjects associated with this classroom.
        """
        subject_ids = self.get_subjects_array()
        return Subject.objects.filter(id__in=subject_ids)
    
    def get_students(self):
        """
        Returns a queryset of students associated with this classroom.
        """
        students_ids = self.get_students_array()
        return CollegeDatabase.objects.filter(id__in=students_ids)
    
    def __str__(self):
        return f"{self.name}"


class ClassRoomForTeacher(models.Model):
    """
    Class for assign the classfor the individual staffs(For teachers)
    """
    class_id = models.ForeignKey(ClassRoom,on_delete=models.CASCADE,null=True)
    staff_id = models.ForeignKey(Staff,on_delete=models.CASCADE,null=True)
    sub_id  = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)

    # def __str__(self):
    #     return
class ModulesForClassRoomForTeacher(models.Model):
    """
    Class for making modules for a classroom
    """
    class_room_staff_id = models.ForeignKey(ClassRoomForTeacher,on_delete=models.CASCADE,null=True)
    assignment_url = models.CharField(max_length=500,null=True)
    module_video_url = models.CharField(max_length=500,null=True)
    
class AttendanInClassroom(models.Model):
    """
    Class for managening the attendence of the students
    """
    class_room_for_staff_id = models.ForeignKey(ClassRoomForTeacher, on_delete=models.CASCADE, null=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)  # Add a reference to the Student model
    date = models.DateField(null=True)
    attendance_status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late')])

    def __str__(self):
        return f"{self.student_id} - {self.date} - {self.attendance_status}"

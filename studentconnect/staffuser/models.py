from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from superadmin.models import RegisterCollege
from collegeadmin.models import Department
# Create your models here.

class ClassRoom(models.Model):
    """
    class for adding the classroom
    """
    college_id = models.ForeignKey(RegisterCollege,on_delete=models.CASCADE)
    name = models.CharField(max_length = 150)
    course = models.ForeignKey(Department,on_delete=models.CASCADE)

    students_ids = models.CharField(
        max_length=255,
        validators=[validate_comma_separated_integer_list],
        blank=True,
        null=True
    )

    def set_students_array(self, integers):
        self.subject_ids = ','.join(map(str, integers))

    def get_students_array(self):
        return list(map(int, filter(None, self.students_ids.split(','))))


    subject_ids = models.CharField(
        max_length=255,
        validators=[validate_comma_separated_integer_list],
        blank=True,
        null=True
    )

    def set_students_array(self, integers):
        self.subject_ids = ','.join(map(str, integers))

    def get_students_array(self):
        return list(map(int, filter(None, self.subject_ids.split(','))))
    
    def __str__(self):
        return f"{self.name}"

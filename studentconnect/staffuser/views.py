from django.forms.models import model_to_dict
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from collegeadmin.serializer import StudentCrudSerilizer, StudentWithDetailsSerializer, CrudSubjectSerilizer
from collegeadmin.serializer import DataValidationSerilzier, ListViewSerilzer
from .serializer import ClassRoomSerilizer, ClassRoomSerializerWithAllData
from collegeadmin.models import Staff, Student, Subject,CollegeDatabase
from .models import *
# Create your views here.


class CrudForClassRoom(viewsets.ModelViewSet):
    """
    class for the crud operation for the classroom
    """
    queryset = ClassRoom.objects.all()
    # permission_classes =[IsAuthenticated]
    serializer_class = ClassRoomSerilizer

    

    def create(self, request, *args, **kwargs):


        college_id = Staff.objects.get(
            user_id=request.GET.get('id', None)).staff.collge_id.id

        try:
            subjects = Subject.objects.filter(
                course=request.data.get('course_id'))
            subjects_ids = list(subjects.values_list('id', flat=True))

            print(subjects_ids)
            print(request.data.get('data'))
        except Subject.DoesNotExist:
            subjects_ids = []

       

        classroom_data = {
            'name': request.data.get('name', ''),
            'course': Department.objects.get(id=request.data.get('course_id')).id,
            'college_id': college_id,
            'students_ids': ','.join(map(str, request.data.get('data', []))),
            'subject_ids': ','.join(map(str, subjects_ids)),
        }

        serializer = ClassRoomSerilizer(data=classroom_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Classroom created successfully'}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.error_messages)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCourse(viewsets.ModelViewSet):
    """
    class for getting the course
    """

    queryset = Department.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = DataValidationSerilzier

    def list(self, request, **kwargs):
        """function for list  the all objects of the departmental model"""
        user_id = request.GET.get('id', None)
        college_instance = Staff.objects.get(user_id=user_id).staff.collge_id
        queryset = Department.objects.filter(college_name=college_instance.id)
        serializer = ListViewSerilzer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetStudents(viewsets.ModelViewSet):
    """
    Class for getting the list of students according to the semester
    """
    queryset = Student.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = StudentCrudSerilizer

    def list(self, request, *args, **kwargs):
        """
        Get function for sorting the students based on semester
        """
        staff_instance = Staff.objects.get(user_id=request.GET.get('id', None))
        college_instance = staff_instance.staff.collge_id
        semester = int(request.GET.get('semseter', 0))
        course = int(request.GET.get('course', 0))
        students = Student.objects.filter(
            student__collge_id=college_instance, semester=semester, course=course)
        serializer = StudentWithDetailsSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetClassRooms(viewsets.ModelViewSet):
    """
    Class for get the classroom Objects 
    """
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializerWithAllData

    def list(self, request, *args, **kwargs):
        user_id = request.GET.get('id')
        college_instance = Staff.objects.get(user_id=user_id).staff.collge_id
        queryset = ClassRoom.objects.filter(college_id=college_instance)

        data = []
        for classroom in queryset:
            classroom_dict = model_to_dict(classroom)

            students_ids = classroom.get_students_array()
            students = CollegeDatabase.objects.filter(id__in=students_ids)
            classroom_dict['students'] = students

            subject_ids = classroom.get_subjects_array()
            subjects = Subject.objects.filter(id__in=subject_ids)
            classroom_dict['subjects'] = subjects

           

            department_ids = [subject['course_id'] for subject in subjects.values()]

            Departments = Department.objects.filter(id__in=department_ids)
            classroom_dict['departments'] = Departments

            data.append(classroom_dict)

        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class GetClassRoom(viewsets.ModelViewSet):
    """
    Class for get the classroom Objects 
    """
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializerWithAllData

    def list(self, request, *args, **kwargs):
        user_id = request.GET.get('id')
        ClassRoom_id = request.GET.get('c_id')
        college_instance = Staff.objects.get(user_id=user_id).staff.collge_id
        queryset = ClassRoom.objects.get(college_id=college_instance,id=ClassRoom_id)

        data = []
        
        classroom_dict = model_to_dict(queryset)

        students_ids = queryset.get_students_array()
        students = CollegeDatabase.objects.filter(id__in=students_ids)
        classroom_dict['students'] = students

        subject_ids = queryset.get_subjects_array()
        subjects = Subject.objects.filter(id__in=subject_ids)
        classroom_dict['subjects'] = subjects

        staff_ids =[subject['staff_id'] for subject in subjects.values()]
        staffs = Staff.objects.filter(id__in=staff_ids)
        
        staff_data_ids=[staff['staff_id'] for staff in staffs.values()]
        staffs_data = CollegeDatabase.objects.filter(id__in=staff_data_ids)
        classroom_dict['staffs_data'] = staffs_data


        department_ids = [subject['course_id'] for subject in subjects.values()]
        Departments = Department.objects.filter(id__in=department_ids)
        classroom_dict['departments'] = Departments

        data.append(classroom_dict)

        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
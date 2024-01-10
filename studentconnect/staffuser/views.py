from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from collegeadmin.models import Staff, Student,Subject
from .serializer import ClassRoomSerilizer
from collegeadmin.serializer import DataValidationSerilzier, ListViewSerilzer
from collegeadmin.serializer import StudentCrudSerilizer,StudentWithDetailsSerializer
# Create your views here.


class CrudForClassRoom(viewsets.ModelViewSet):
    """
    class for the crud operation for the classroom
    """
    queryset = ClassRoom.objects.all()
    # permission_classes =[IsAuthenticated]
    serializer_class = ClassRoomSerilizer

    def create(self, request, *args, **kwargs):
       
        college_id = Staff.objects.get(user_id=request.GET.get('id', None)).staff.collge_id

        try:
            subjects = Subject.objects.filter(course=request.data['course_id'])
            subjects_ids = list(subjects.values_list('id', flat=True))
            print(subjects_ids)
            print(request.data['data']) 
        except Subject.DoesNotExist:
            subjects_ids = []

        classroom_data = {
            'name': request.data['name'],  
            'course': Department.objects.get(id=request.data['course_id']),  
            'college_id': college_id,
            'students_ids': request.data['data'] , 
            'subject_ids': subjects_ids,
        }

        serializer = ClassRoomSerilizer(data=classroom_data)

        print(serializer)

        if serializer.is_valid():
        
            serializer.save()
            return Response({'message': 'Classroom created successfully'}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # classroom_instance = ClassRoom.objects.create(**classroom_data)

        # return Response(status=status.HTTP_200_OK)

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
        print(request.GET.get('id', None))
        print(request.GET)

        # Assuming 'college_id' is a field in the Staff model
        staff_instance = Staff.objects.get(user_id=request.GET.get('id', None))
        college_instance = staff_instance.staff.collge_id

        # Convert semester and course to integers
        semester = int(request.GET.get('semseter', 0))
        course = int(request.GET.get('course', 0))

        print(semester)
        print(course)

        # Filter students using integers
        students = Student.objects.filter(student__collge_id=college_instance, semester=semester, course=course)
        serializer = StudentWithDetailsSerializer(students, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

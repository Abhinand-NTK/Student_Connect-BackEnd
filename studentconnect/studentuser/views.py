from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from staffuser.models import ClassRoom
from collegeadmin.models import Student
from rest_framework.response import Response
from staffuser.serializer import ClassRoomSerilizer
from .serializer import SerializerForGetSubjectsInstudentSide
from collegeadmin.serializer import CrudSubjectSerilizer
from rest_framework.permissions import IsAuthenticated
from collegeadmin.serializer import CrudSubjectSerilizer


# Create your views here.


class GetsubjectsToStudent(ModelViewSet):
    """
    Class for showing the subjects of the students in the forntend
    """
    queryset = ClassRoom.objects.all()
    serializer_class = SerializerForGetSubjectsInstudentSide
    # permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """
        Funtion for get the list of the subjects in the student user side
        """
        user_id = self.kwargs.get('pk')
        id = Student.objects.get(user_id=user_id).student
        student = ClassRoom.objects.get(students_ids__contains=id.id)
        serializer_for_classroom = ClassRoomSerilizer(student)
        subjects = student.get_subjects()
        serializer = CrudSubjectSerilizer(subjects, many=True)
        print(serializer_for_classroom.data)
        print(serializer.data)
        response_data = {
            'classroom': serializer_for_classroom.data,
            'subjects': serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

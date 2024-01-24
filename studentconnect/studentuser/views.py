from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from staffuser.models import ClassRoom, ModulesForClassRoomForTeacher,AttendanInClassroom
from collegeadmin.models import Student,Subject,RequestForLeave,CollegeDatabase,Staff
from superadmin.models import UserAccount
from rest_framework.response import Response
from staffuser.serializer import ClassRoomSerilizer,SerilizerForAttendenceManagement,ClassRoomForTeacherSerializerGet, SerilierClassforModulesForClassRoomForTeacher,ClassRoomForTeacher
from .serializer import SerializerForGetSubjectsInstudentSide,SerilizerForLeaveReqeust
from collegeadmin.serializer import CrudSubjectSerilizer
from rest_framework.permissions import IsAuthenticated
from collegeadmin.serializer import CrudSubjectSerilizer
from collections import defaultdict
from django.http import JsonResponse


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
        response_data = {
            'classroom': serializer_for_classroom.data,
            'subjects': serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class VideosAssignmentForStudent(ModelViewSet):
    """
    class for retrive the videos and the files in the class
    """
    queryset = ModulesForClassRoomForTeacher.objects.all()
    serializer_class = SerilierClassforModulesForClassRoomForTeacher
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        Class for retrive the class 
        """
        class_room_staff_id = request.GET.get('class_room_staff_id')
        sub_id = request.GET.get('sub_id')
        print(class_room_staff_id,sub_id)
        media_instance = ClassRoomForTeacher.objects.filter(class_id=class_room_staff_id,
                                                                      sub_id=sub_id).first()
        if media_instance:
            modules_for_classroom = media_instance.modulesforclassroomforteacher_set.all()
            print(modules_for_classroom)
            serializer = SerilierClassforModulesForClassRoomForTeacher(modules_for_classroom,many=True)
            print("The data :---",media_instance)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({"detail": "There is nothing right now."},status=status.HTTP_204_NO_CONTENT)


class StudentAttendence(ModelViewSet):
    """
    Class for fetech the details of the students attendence
    """
    queryset = AttendanInClassroom.objects.all()
    serializer_class = SerilizerForAttendenceManagement
    # permission_classes = [IsAuthenticated]
    def retrieve(self, request, *args, **kwargs):
        """
        Funtion that will retrive the students and there attendence
        """

        user_id = self.kwargs.get('pk')
        UserAccount.objects.get(id=user_id)
        student_instance = Student.objects.get(user_id=user_id)
        # Subjects = Subject.objects.filter(semseter=student_instance.semester, course=student_instance.course)
        # subjectNames = [subject.name for subject in Subjects]
        attendance_data = defaultdict(lambda: {'present': 0, 'total': 0})
        Attendances = AttendanInClassroom.objects.select_related('student_id', 'class_room_for_staff_id__sub_id').filter(student_id__user_id=user_id)
        # Update the attendance_data based on Attendances
        for attendance in Attendances:
            subject_name = attendance.class_room_for_staff_id.sub_id.name
            attendance_data[subject_name]['total'] += 1
            if attendance.attendance_status == 'present':
                attendance_data[subject_name]['present'] += 1

        # Calculate the percentage for each subject
        percentage_data = {subject_name: {'subject': subject_name, 'percentage': (data['present'] / data['total']) * 100 if data['total'] > 0 else 0}
                           for subject_name, data in attendance_data.items()}

        # Create the final result dictionary
        result_dict = {'name': f"{student_instance.student.first_name}  {student_instance.student.last_name}", 'subjects': percentage_data}

        # Return the result as JSON response
        return JsonResponse(result_dict, status=status.HTTP_200_OK)
      

class LeaveRequest(ModelViewSet):
    """
    Class for managining the leave request
    """
    queryset = RequestForLeave.objects.all()
    serializer_class = SerilizerForLeaveReqeust
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """"
        Funtion for retrive the objects in the class
        """
        id = self.kwargs.get('pk')
        queryset = RequestForLeave.objects.filter(requestor = id)
        serializer = SerilizerForLeaveReqeust(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def list(self, request, *args, **kwargs):
        """
        Funtion for retrieving the all the requests from the staffs and the students
        """
        user_id = request.GET.get('id')
        college_id = Staff.objects.get(user_id=user_id).staff.collge_id_id
        queryset = RequestForLeave.objects.filter(requestor__collge_id = college_id)
        serializer = SerilizerForLeaveReqeust(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Function for approval of the leave requests
        """
        user_id = request.GET.get('id')
        college_id = Staff.objects.get(user_id=user_id).staff.collge_id_id
        queryset = RequestForLeave.objects.filter(requestor__collge_id = college_id) 
        id = self.kwargs.get('pk')
        instance = self.get_object()
        instance.approval_status = not instance.approval_status
        instance.save()
        serializer = SerilizerForLeaveReqeust(queryset,many=True)


        return Response(serializer.data,status=status.HTTP_200_OK)
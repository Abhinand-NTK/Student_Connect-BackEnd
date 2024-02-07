from .task import send_email_to_users
from django.forms.models import model_to_dict
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from collegeadmin.serializer import StudentCrudSerilizer, StudentWithDetailsSerializer, CrudSubjectSerilizer
from collegeadmin.serializer import DataValidationSerilzier, ListViewSerilzer
from .serializer import SerilierClassforModulesForClassRoomForTeacher, StudentUsersProfileSerilizer, SerilizerForAttendenceManagement, ClassRoomForTeacherSerializerGet, ClassRoomForTeacherSerializers, ClassRoomForTeacherSerializer, ClassRoomSerilizer, ClassRoomSerializerWithAllData, StaffUserProfileSerilizer, ClassRoomSerilizerGet
from collegeadmin.models import Staff, Student, Subject, CollegeDatabase
from .models import *
# Create your views here.


class CrudForClassRoom(viewsets.ModelViewSet):
    """
    class for the crud operation for the classroom
    """
    queryset = ClassRoom.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ClassRoomSerilizer

    def create(self, request, *args, **kwargs):

        college_id = Staff.objects.get(
            user_id=request.GET.get('id', None)).staff.collge_id.id

        try:
            subjects = Subject.objects.filter(
                course=request.data.get('course_id'))
            subjects_ids = list(subjects.values_list('id', flat=True))

        except Subject.DoesNotExist:
            subjects_ids = []

        classroom_data = {
            'name': request.data.get('name', ''),
            'course': Department.objects.get(id=request.data.get('course_id')).id,
            'college_id': college_id,
            'students_ids': ','.join(map(str, request.data.get('data', []))),
            'subject_ids': ','.join(map(str, subjects_ids)),
            'semester': subjects.first().semseter,
        }

        serializer = ClassRoomSerilizer(data=classroom_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Classroom created successfully'}, status=status.HTTP_201_CREATED)
        else:

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
        Updates the students details in the class 
        """
        data = request.data.copy()  # Create a copy of request data

        classroom_id = self.kwargs['pk']
        student_ids = ','.join(map(str, data.get('student_ids', [])))

        try:
            classroom = ClassRoom.objects.get(id=classroom_id)
        except ClassRoom.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        classroom.students_ids = student_ids
        classroom.save()

        return Response(status=status.HTTP_200_OK)
    
class BlcokClass(viewsets.ModelViewSet):
    """
    Blocking the class 
    """
    def create(self, request, *args, **kwargs):
        """
        Funtion for active and deactive the classroom
        """
        class_id = request.data.get('id')
            
        try:
            classroom = ClassRoom.objects.get(id=class_id)
        except ClassRoom.DoesNotExist:
            return Response({'error': 'ClassRoom with the specified ID does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Toggle the active status
        classroom.active = not classroom.active
        classroom.save()
        
        return Response({'success': f'ClassRoom {class_id} status has been updated successfully.'}, status=status.HTTP_200_OK)

class GetCourse(viewsets.ModelViewSet):
    """
    class for getting the course
    """

    queryset = Department.objects.all()
    permission_classes = [IsAuthenticated]
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
        students_meeting_criteria = Student.objects.filter(
            student__collge_id=college_instance, semester=semester, course=course)

        students_ids = [str(student.student_id)
                        for student in students_meeting_criteria]

        if ClassRoom.objects.exists():
            students_ids = [student_id for student_id in students_ids if not ClassRoom.objects.filter(
                students_ids__contains=student_id).exists()]
            students_meeting_criteria = Student.objects.filter(
                student__id__in=students_ids)

        serializer = StudentWithDetailsSerializer(
            students_meeting_criteria, many=True)
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

            department_ids = [subject['course_id']
                              for subject in subjects.values()]

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
        queryset = ClassRoom.objects.get(
            college_id=college_instance, id=ClassRoom_id)

        data = []

        classroom_dict = model_to_dict(queryset)

        students_ids = queryset.get_students_array()
        students = CollegeDatabase.objects.filter(id__in=students_ids)
        classroom_dict['students'] = students

        subject_ids = queryset.get_subjects_array()
        subjects = Subject.objects.filter(id__in=subject_ids)
        classroom_dict['subjects'] = subjects

        staff_ids = [subject['staff_id'] for subject in subjects.values()]
        staffs = Staff.objects.filter(id__in=staff_ids)

        staff_data_ids = [staff['staff_id'] for staff in staffs.values()]
        staffs_data = CollegeDatabase.objects.filter(id__in=staff_data_ids)
        classroom_dict['staffs_data'] = staffs_data

        department_ids = [subject['course_id']
                          for subject in subjects.values()]
        Departments = Department.objects.filter(id__in=department_ids)
        classroom_dict['departments'] = Departments

        data.append(classroom_dict)

        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StaffUserProfileCrudView(viewsets.ModelViewSet):
    """
    Class for Crud the user data
    """
    queryset = Staff.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = StaffUserProfileSerilizer

    def retrieve(self, request, *args, **kwargs):
        """Function for get the list of the staff users in the database of the specific colleges"""
        user_id = self.kwargs.get('pk')
        try:
            staff_instance = Staff.objects.get(user_id=user_id)
            serializer = self.get_serializer(staff_instance)

        except Staff.DoesNotExist:
            try:
                student_instance = Student.objects.get(user_id=user_id)
                serializer = StudentUsersProfileSerilizer(student_instance)

            except Student.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """funtion for update the info of the user"""
        user_id = self.kwargs.get('pk')
        try:
            staff_instance = Staff.objects.get(user_id=user_id).staff
        except Staff.DoesNotExist:
            try:
                staff_instance = Student.objects.get(user_id=user_id).student
            except Student.DoesNotExist:
                staff_instance = None

        user_image = request.FILES.get('image')

        print(user_image)

        if user_image:
            staff_instance.user_image = user_image
            staff_instance.save()

            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)


class GetPro(viewsets.ModelViewSet):
    """
    Class 
    """
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerilizer

    def list(self, request, *args, **kwargs):
        """function for get the details of the individual teacher"""
        values_str = request.GET.get('sub_ids', '')
        result_dict = {}

        classrooms_with_subjects = ClassRoom.objects.filter(
            subject_ids__contains=values_str)
        for classroom in classrooms_with_subjects:
            sub_array = classroom.get_subjects_array()
            subjects = Subject.objects.filter(id__in=sub_array)
            serialized_subjects = CrudSubjectSerilizer(
                subjects, many=True).data
            result_dict[classroom.name] = {'Subjects': serialized_subjects}

        serializer_2 = ClassRoomSerilizerGet(
            classrooms_with_subjects, many=True)
        # serializer = self.get_serializer(classrooms_with_subjects, many=True)

        data = {
            "data1": serializer_2.data,
            "data2": result_dict,
        }
        return Response(data, status=status.HTTP_200_OK)


class ClassRoomAssignCrudView(viewsets.ModelViewSet):
    """
    Class for Crud the Classroom Allocation of Teachers
    """
    queryset = ClassRoomForTeacher.objects.all()
    serializer_class = ClassRoomForTeacherSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """"
        Get function for the class view
        """
        id = request.GET.get('id', None)

        values_str = request.GET.get('sub_idss', '')

        classrooms_with_subjects = ClassRoom.objects.filter(
            subject_ids__contains=values_str)
        classroom_for_teacher_objects = ClassRoomForTeacher.objects.filter(
            class_id__in=classrooms_with_subjects)
        classroom_dict1 = {
            classroom.class_id.name: classroom.id for classroom in classroom_for_teacher_objects}

        classroom_dict = {}

        for classroom in classroom_for_teacher_objects:
            subject_name = classroom.sub_id.name
            print(classroom.sub_id.name, "--------->>>>>>>.")
            class_name = classroom.class_id.name
            classroom_id = classroom.id

            if subject_name not in classroom_dict:
                classroom_dict[subject_name] = {}

            classroom_dict[subject_name][class_name] = classroom_id

        serializer = ClassRoomForTeacherSerializerGet(
            classroom_for_teacher_objects, many=True)
        return Response(classroom_dict, status=status.HTTP_200_OK)


class GetViewForClassRoomForTeacher(viewsets.ModelViewSet):
    """
    Class for the ClassRoomForTeacher Model
    """
    queryset = ClassRoomForTeacher.objects.all()
    serializer_class = ClassRoomForTeacherSerializers
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrive the objects of the class for a particular user
        """
        user_id = self.kwargs.get('pk')
        # staff = Staff.objects.get(id=user_id)
        data = self.queryset.filter(staff_id=user_id,class_id__active=True)
        for i in data:
            subjects_idss = i.class_id.get_students()
            # print(subjects_ids)
            print(subjects_idss)

        serializer = self.serializer_class(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AttendenceForStudents(viewsets.ModelViewSet):
    """
    Class for mark the attendence of the students
    """
    queryset = AttendanInClassroom.objects.all()
    serializer_class = SerilizerForAttendenceManagement
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Function to handle attendance of students via a POST request
        """

        attendance_data = request.data
        response_messages = []

        for item in attendance_data:
            item['student_id'] = Student.objects.get(
                student=item['student_id']).id
        response_data = []
        for item_data in attendance_data:
            # Check if the resource already exists based on some criteria
            instance = AttendanInClassroom.objects.filter(class_room_for_staff_id=item_data['class_room_for_staff_id'],
                                                          student_id=item_data['student_id'],
                                                          date=item_data['date']).first()

            if instance:
                # If the resource exists, update it
                serializer = self.get_serializer(instance, data=item_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                response_data.append(serializer.data)
            else:
                # If the resource doesn't exist, create it
                serializer = self.get_serializer(data=item_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                response_data.append(serializer.data)

        return Response(response_data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        """
        Retrieve the total attendance list of the students using id of that classroom, class_room_for_staff_id, and date
        """
        class_room_id = request.GET.get('class_room_for_staff_id')
        date = request.GET.get('date')

        if not class_room_id or not date:
            return Response({'error': 'class_room_for_staff_id and date are required parameters'}, status=status.HTTP_400_BAD_REQUEST)

        # Filter the queryset based on class_room_for_staff_id and date
        data = self.queryset.filter(
            class_room_for_staff_id=class_room_id,
            date=date
        )

        # Serialize the data
        serializer = self.serializer_class(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CrudForModules(viewsets.ModelViewSet):
    """
    Class for the making the modules for the videos
    """
    queryset = ModulesForClassRoomForTeacher.objects.all()
    serializer_class = SerilierClassforModulesForClassRoomForTeacher
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        """
        Function call for saving the url instance of the video
        """
        item = request.data
        print(self.kwargs.get('pk'))
        id = self.kwargs.get('pk')
        instance = ModulesForClassRoomForTeacher.objects.get(
            id=id, class_room_staff_id=item['class_room_staff_id'])
        students = instance.class_room_staff_id.class_id.get_students()
        students_mail = []
        for student in students:
            students_mail.append(student.email)
        print(students_mail)
        send_email_to_users(students_mail)
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def destroy(self, request, *args, **kwargs):
    #     """
    #     Function for delete the instance in the class
    #     """
    #     id = self.queryset.Objects.get(id)

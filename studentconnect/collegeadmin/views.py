from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from superadmin.models import RegisterCollege
from .models import CollegeDatabase
from .models import Department, Staff, Subject, Session, Student
from .serializer import * 


class CrudCourseView(viewsets.ModelViewSet):
    """
    View For Adding The Course in The College 
    """
    queryset = Department.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = DataValidationSerilzier

    def create(self, request):
        """function for creating the subject """
        user_id = request.data.get('id')
        college = RegisterCollege.objects.get(user_details=user_id)
        permission_classes = [IsAuthenticated]

        department_data = {
            'coursename': request.data.get('coursename'),
            'college_name': college.id
        }

        serilizer = DataValidationSerilzier(data=department_data)
        serilizer.Meta.model = Department
        if serilizer.is_valid():
            instance = serilizer.save()
            return Response(serilizer.data, status=status.HTTP_201_CREATED)
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """function for updating  the instance of the departmental model"""
        serilizer = DataValidationSerilzier(data=request.data)
        serilizer.Meta.model = Department
        id = request.data['edit']
        instance = Department.objects.get(id=id)
        serializer = DataValidationSerilzier(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, **kwargs):
        """function for list  the all objects of the departmental model"""
        user_id = request.GET.get('id', None)
        college_instance = RegisterCollege.objects.get(user_details=user_id)

        queryset = Department.objects.filter(college_name=college_instance.id)
        serializer = ListViewSerilzer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CrudStaffView(viewsets.ModelViewSet):
    """
    Class for doing the CRUD operations on the staff
    """
    queryset = CollegeDatabase.objects.all()
    serializer_class = CrudStaffSerilizer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """The function for making an object for the staff and the CollegeDatabase model"""
        data = request.data
        college_id = RegisterCollege.objects.get(
            user_details=request.data.get('id')).id

        data.update({'collge_id':  college_id})
        serilizer = CrudStaffSerilizer(
            data=request.data)  
        if serilizer.is_valid():
            instance = serilizer.save()
            instance_staff = Staff.objects.create(staff=instance)
            instance_staff.save()
            return Response(serilizer.data, status=status.HTTP_201_CREATED)
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """function for updating  the instance of the staffmodel model"""
        serilizer = CrudStaffSerilizer(data=request.data)
        id = request.data['edit']
        instance = CollegeDatabase.objects.get(id=id)
        serializer = CrudStaffSerilizer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, **kwargs):
        """Function for getting the staffs in a college"""
        user_id = request.GET.get('id', None)
        college_instance = RegisterCollege.objects.get(user_details=user_id)

        queryset = CollegeDatabase.objects.filter(
            collge_id=college_instance.id)
        serializer = CrudStaffSerilizer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CrudSubjectView(viewsets.ModelViewSet):
    """
    class for adding the CrudSubjects
    """

    queryset = Subject.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CrudSubjectSerilizer

    def create(self, request, *args, **kwargs):
        """function for adding the subject """
        college_instance = CollegeDatabase.objects.get(
            id=request.data.get('staff'))
        data = request.data
        data.update({'staff':  college_instance.staff.id})
        serilizer = CrudSubjectSerilizer(
            data=request.data)  
        if serilizer.is_valid():
            instance = serilizer.save()
            return Response(serilizer.data, status=status.HTTP_201_CREATED)
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """Function for edit the subject"""
        serilizer = CrudSubjectSerilizer(data=request.data)
        id = request.data['edit']
        instance = Subject.objects.get(id=id)
        serializer = CrudSubjectSerilizer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """function for send all the subjects to the fronend"""

        user_id = request.GET.get('id', None)
        college_instance = RegisterCollege.objects.get(user_details=user_id)

        queryset = Subject.objects.filter(
            course__college_name=college_instance.id)
        serializer = CrudSubjectSerilizer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SessionCrudView(viewsets.ModelViewSet):
    """
    class for adding the session for specific acadamic year
    """
    queryset = Session.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CrudSessionSerilzer

    def create(self, request):
        """Function for adding the session"""
        college_instance = RegisterCollege.objects.get(
            user_details=request.data.get('id'))
        data = request.data
        data.update({'college_id':  college_instance.id})
        serilizer = CrudSessionSerilzer(
            data=request.data)  
        if serilizer.is_valid():
            instance = serilizer.save()
            return Response(serilizer.data, status=status.HTTP_201_CREATED)
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """Function for getting the details of the session"""

        user_id = request.GET.get('id', None)
        college_instance = RegisterCollege.objects.get(user_details=user_id)

        queryset = Session.objects.filter(college_id=college_instance)
        serilizer = CrudSessionSerilzer(queryset, many=True)
        return Response(serilizer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """Function for edit the session"""
        serilizer = CrudSessionSerilzer(data=request.data)
        id = request.data['edit']
        instance = Session.objects.get(id=id)
        serializer = CrudSessionSerilzer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class StudentCrudView(viewsets.ModelViewSet):
    """Class for Crud View"""

    queryset = Subject.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = CrudStaffSerilizer

    def create(self, request, *args, **kwargs):
        """Function for adding the student"""
        data = request.data
        college_id = RegisterCollege.objects.get(
            user_details=request.data.get('id')).id
        course_id = Department.objects.get(id=request.data['course'])
        session_id = Session.objects.get(id=request.data['session'])
        #here i used update funtion for adding the college id to  add a key value in to the dict
        data.update({'collge_id':  college_id})
        serilizer = CrudStaffSerilizer(
            data=request.data)  
        if serilizer.is_valid():
            instance = serilizer.save()
            instance_student = Student.objects.create(
                student=instance,
                course=course_id,
                session=session_id,
            )
            return Response(serilizer.data, status=status.HTTP_201_CREATED)
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, *args, **kwargs):
        """The function is using to update the student object"""

        print(request)
        serilizer = CrudStaffSerilizer(data=request.data)
        id = request.data['edit']
        instance = CollegeDatabase.objects.get(id=id)
        serializer = CrudStaffSerilizer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request, *args, **kwargs):
        """The function for getting the list of the student"""
        id = request.GET.get('id', None)
        college_instance = RegisterCollege.objects.get(user_details=id)
        students_with_details = Student.objects.select_related('student').filter(student__collge_id=college_instance)
        serializer = StudentWithDetailsSerializer(students_with_details, many=True)
        data = serializer.data  # Get serialized data
        return Response(data, status=status.HTTP_200_OK)  # Return a Response instance
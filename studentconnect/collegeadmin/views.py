from django.utils.crypto import get_random_string
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from superadmin.models import RegisterCollege, UserAccount
from .models import CollegeDatabase
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Department, Staff, Subject, Session, Student
from superadmin.serializer import UserDetailsSerilzer
from .serializer import *
from django.core.exceptions import ObjectDoesNotExist


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
        id = request.GET.get('id', None)
        college_instance = RegisterCollege.objects.get(user_details=id)
        staff_with_details = Staff.objects.select_related(
            'staff').filter(staff__collge_id=college_instance)
        serializer = StaffWithDetailsSerializer(staff_with_details, many=True)
        data = serializer.data  # Get serialized data
        # Return a Response instance
        return Response(data, status=status.HTTP_200_OK)


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
        college_instance = CollegeDatabase.objects.get(
            id=request.data.get('staff'))
        data = request.data
        data.update({'staff':  college_instance.staff.id})
        instance = Subject.objects.get(id=id)
        print(instance)
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
        serializer = SubjectDetailSerializer(queryset, many=True)

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
    permission_classes = [IsAuthenticated]
    serializer_class = CrudStaffSerilizer

    def create(self, request, *args, **kwargs):
        """Function for adding the student"""
        data = request.data
        college_id = RegisterCollege.objects.get(
            user_details=request.data.get('id')).id
        course_id = Department.objects.get(id=request.data['course'])
        session_id = Session.objects.get(id=request.data['session'])
        # here i used update funtion for adding the college id to  add a key value in to the dict
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
        students_with_details = Student.objects.select_related(
            'student').filter(student__collge_id=college_instance)
        serializer = StudentWithDetailsSerializer(
            students_with_details, many=True)
        data = serializer.data  # Get serialized data
        # Return a Response instance
        return Response(data, status=status.HTTP_200_OK)


class CreatingUsersView(viewsets.ModelViewSet):
    """
    Class for creating the users according to the user type
    """
    queryset = UserAccount.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = UserDetailsSerilzer

 

    # def create(self, request, *args, **kwargs):

    #     print("The data is this>>>>>>>>>>",request.data)

    #     try:
    #         user_details = Student.objects.get(student__id=request.data['edit'])
    #     except ObjectDoesNotExist:

    #         pass

    #     if not user_details.student.email_sent:

    #         print(user_details.student.email)

    #         user = UserAccount.objects.create(
    #             first_name=user_details.student.first_name,
    #             last_name=user_details.student.last_name,
    #             email=user_details.student.email,
    #             user_type=3,
    #         )
    #         user.save()

    #         password = get_random_string(length=8)
    #         user.set_password(password)
    #         user.save()

    #         print(password)
    #         user_details.student.email_sent = True
    #         user_details.student.primary_password = password
    #         user_details.student.save()


    #         # Sending the confirmation mail while creating the account by super admin
    #         login_link = f'http://localhost:5173/signin'
    #         subject = 'College Registration Request Received'
    #         template_path = 'StudentAccountCreateSuccessMail.html'
    #         context = {
    #             'student_name': user.first_name,
    #             'student_username': user.email,
    #             # 'college_name': user_details.staff.collge_id.collegename,
    #             'student_password': user_details.student.collge_id.primary_password,
    #             'student_login_link': login_link,
    #             'support_contact': '[Your Support Email or Phone Number]',
    #             'platform_name': '[Your Platform Name]',
    #             'company_name': '[Your Company/Organization Name]',
    #         }
    #         html_message = render_to_string(template_path, context)
    #         plain_message = strip_tags(html_message)

    #         send_mail(
    #             subject,
    #             plain_message,
    #             settings.DEFAULT_FROM_EMAIL,
    #             [user.email],
    #             html_message=html_message,
    #         )

    #         return Response({'message': 'Activation email sent successfully.'}, status=status.HTTP_200_OK)
        

    #     else:
    #         user_details = Staff.objects.get(staff__id=request.data['id'])
    #         user = UserAccount.objects.create(
    #             first_name=user_details.staff.first_name,
    #             last_name=user_details.staff.last_name,
    #             email=user_details.staff.email,
    #             user_type=2,
    #         )

    #         user_details.staff.primary_password = password
    #         user_details.staff.email_sent = True
    #         user_details.save()

    #         password = get_random_string(length=8)
    #         user.set_password(password)
    #         user.save()

    #         # Sending the confirmation mail while creating the account by super admin
    #         login_link = f'http://localhost:5173/signin'
    #         subject = 'College Registration Request Received'
    #         template_path = 'StaffAccountCreateSuccessMail.html'
    #         context = {
    #             'staff_name': user.first_name,
    #             'new_staff_username': user.email,
    #             # 'college_name': user_details.staff.collge_id.collegename,
    #             'new_staff_password': user_details.staff.collge_id.primary_password,
    #             'student_login_link': login_link,
    #             'support_contact': '[Your Support Email or Phone Number]',
    #             'platform_name': '[Your Platform Name]',
    #             'company_name': '[Your Company/Organization Name]',
    #         }
    #         html_message = render_to_string(template_path, context)
    #         plain_message = strip_tags(html_message)

    #         send_mail(
    #             subject,
    #             plain_message,
    #             settings.DEFAULT_FROM_EMAIL,
    #             [user.email],
    #             html_message=html_message,
    #         )
            

    #         user.save()
    #         return Response({'message': 'Activation email sent successfully.'}, status=status.HTTP_200_OK)
    def create(self, request, *args, **kwargs):
        print("The data is this>>>>>>>>>>", request.data)

        try:
            user_details = Student.objects.get(student__id=request.data.get('edit'))
        except ObjectDoesNotExist:
            # If student account doesn't exist, create a staff account
            try:
                user_details = Staff.objects.get(staff__id=request.data.get('edit'))
            except ObjectDoesNotExist:
                return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

            if user_details.staff.email_sent:
                return Response({'message': 'Staff account already created.'}, status=status.HTTP_400_BAD_REQUEST)

            # Staff Account Creation
            user = UserAccount.objects.create(
                first_name=user_details.staff.first_name,
                last_name=user_details.staff.last_name,
                email=user_details.staff.email,
                user_type=2,
            )

            password = get_random_string(length=8)
            user.set_password(password)
            user.save()

            user_details.staff.primary_password = password
            user_details.staff.email_sent = True
            user_details.staff.save()

            # Sending the confirmation mail while creating the account by super admin
            login_link = 'http://localhost:5173/signin'  # Change as needed
            subject = 'College Registration Request Received'
            template_path = 'StaffAccountCreateSuccessMail.html'  # Adjust the template path
            context = {
                'staff_name': user.first_name,
                'new_staff_username': user.email,
                'new_staff_password': user_details.staff.primary_password,
                'student_login_link': login_link,
                'support_contact': '[Your Support Email or Phone Number]',
                'platform_name': '[Your Platform Name]',
                'company_name': '[Your Company/Organization Name]',
            }
            html_message = render_to_string(template_path, context)
            plain_message = strip_tags(html_message)

        else:
            # Student Account Creation
            if user_details.student.email_sent:
                return Response({'message': 'Student account already created.'}, status=status.HTTP_400_BAD_REQUEST)

            # Student Account Creation
            user = UserAccount.objects.create(
                first_name=user_details.student.first_name,
                last_name=user_details.student.last_name,
                email=user_details.student.email,
                user_type=3,
            )

            password = get_random_string(length=8)
            user.set_password(password)
            user.save()

            print(password)
            user_details.student.email_sent = True
            user_details.student.primary_password = password
            user_details.student.save()

            # Sending the confirmation mail while creating the account by super admin
            login_link = 'http://localhost:5173/signin'  # Change as needed
            subject = 'College Registration Request Received'
            template_path = 'StudentAccountCreateSuccessMail.html'  # Adjust the template path
            context = {
                'student_name': user.first_name,
                'student_username': user.email,
                'student_password': user_details.student.primary_password,
                'student_login_link': login_link,
                'support_contact': '[Your Support Email or Phone Number]',
                'platform_name': '[Your Platform Name]',
                'company_name': '[Your Company/Organization Name]',
            }
            html_message = render_to_string(template_path, context)
            plain_message = strip_tags(html_message)

        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
        )

        return Response({'message': 'Activation email sent successfully.'}, status=status.HTTP_200_OK)
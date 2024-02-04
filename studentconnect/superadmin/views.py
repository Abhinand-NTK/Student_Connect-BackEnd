

from rest_framework import viewsets, status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.crypto import get_random_string
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .serializer import RegisterCollegeSerilzer, MyTokenSerilizer, UserDetailsSerilzer, CollegeDetailsSerilizer, UpdateCollegeSerializer
from .models import RegisterCollege, UserAccount
import smtplib
from email.mime.text import MIMEText
import secrets


class CollegeRegisterViewSet(viewsets.ModelViewSet):

    """
    Your view class description.
    """
    # Define permission classes at the class level
    queryset = RegisterCollege.objects.all()
    permission_classes = []
    serializer_class = RegisterCollegeSerilzer

    def create(self, request, *args, **kwargs):
        serializer = RegisterCollegeSerilzer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            subject = 'College Registration Request Received'
            template_path = 'PrimeryEmailForAdminUser.html'
            context = {
                'user_name': instance.collegename,
                'college_name': instance.collegename,
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
                [instance.email],
                html_message=html_message,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollegeUpdateViewSet(viewsets.ModelViewSet):

    """
    Class View for Update the College Details
    """
    queryset = RegisterCollege.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = UpdateCollegeSerializer

    def update(self, request, *args, **kwargs):
        college_id = kwargs.get('pk')

        try:
            college = RegisterCollege.objects.get(id=college_id)

            # Toggle is_active and is_activate fields
            college.user_details.is_active = not college.user_details.is_active
            college.is_activate = not college.is_activate

            college.user_details.save()
            college.save()

            # Fetch all colleges and serialize the entire queryset
            all_colleges = RegisterCollege.objects.all()
            serializer = UpdateCollegeSerializer(all_colleges, many=True)

            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

        except RegisterCollege.DoesNotExist:
            return Response({'message': 'College not found.'}, status=status.HTTP_404_NOT_FOUND)


class CollegeListViewSet(viewsets.ModelViewSet):

    """
    Your view class description.
    """
    queryset = RegisterCollege.objects.all()
    serializer_class = RegisterCollegeSerilzer


class MyTokenObtainPairView(TokenObtainPairView):

    """
    Your view class description.
    """
    serializer_class = MyTokenSerilizer
    throttle_scope = 'login'


class UserDetails(viewsets.ModelViewSet):

    """
    ViewSet for getting details of the user.
    """

    queryset = UserAccount.objects.all()
    serializer_class = UserDetailsSerilzer
    permission_classes = [IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CollegeDetails(viewsets.ModelViewSet):

    """
    ViewSet for getting details of the Collges that is registerd by the users.
    """

    queryset = RegisterCollege.objects.all()

    serializer_class = CollegeDetailsSerilizer
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = RegisterCollege.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Send_Account_Activation_Mail(viewsets.ModelViewSet):

    """
    viewset for activating the college admin 
    """

    queryset = RegisterCollege.objects.all()
    serializer_class = CollegeDetailsSerilizer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        try:
            college_id = request.data.get('id')
            # Convert college_id to an integer

            # Getting the RegisterCollegeModel
            college = RegisterCollege.objects.get(id=college_id)

            if not college.Verfication_email_status:
                # Creating an Account for the college using the random
                # password and make the user_type as the collegeadmin
                admin_account = UserAccount.objects.create(
                    email=college.email,
                    is_active=True,  # Change to is_active instead of is_activate
                    user_type=1
                )

                password = get_random_string(length=8)
                admin_account.set_password(password)
                admin_account.save()

                # Saving the details of the admin in the college database
                college.primary_password = password
                college.Verfication_email_status = True
                college.user_details = admin_account
                college.save()

                # Sending the confirmation mail while creating the account by super admin
                login_link = f'http://localhost:5173/'
                subject = 'College Registration Request Received'
                template_path = 'Conformation_mail_to_collage_Admin.html'
                context = {
                    'user_name': college.email,
                    'college_name': college.collegename,
                    'primary_password': college.primary_password,
                    'login_link': login_link,
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
                    [college.email],
                    html_message=html_message,
                )

                return Response({'message': 'Activation email sent successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'College already activated.'}, status=status.HTTP_400_BAD_REQUEST)

        except RegisterCollege.DoesNotExist:
            return Response({'message': 'College not found.'}, status=status.HTTP_404_NOT_FOUND)


class CheckSubscription(viewsets.ModelViewSet):
    """
    check subscription status
    """

    def retrieve(self, request, *args, **kwargs):
        """
        Funtion for rertive the college details
        """

        id = request.user.id

        stat = RegisterCollege.objects.get(user_details=id)

        serilizer = RegisterCollegeSerilzer(stat)

        return Response(serilizer.data, status=status.HTTP_200_OK)




def genretetopo(length=6):
    """
    Generate a random OTP of the specified length.
    """
    otp = ''.join(secrets.choice('0123456789') for _ in range(length))
    return otp


class OtpRequest(viewsets.ModelViewSet):
    """
    Class for genrateotp
    """

    queryset = UserAccount.objects.all()
    serializer_class = UserDetailsSerilzer


    def create(self, request, *args, **kwargs):
        """
        Function for sending the OTP
        """

        print()
        email = request.data.get('data')  # Use get to avoid KeyError if 'email' is not present
        user = None
        try:
            user = UserAccount.objects.get(email=email['username'])
        except UserAccount.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        # Assuming you have a function named genretetopo that generates the OTP
        otp = genretetopo()

        # Save the OTP to the user
        user.otp = otp
        user.save()

        # Send email with the OTP
        subject = 'Your OTP for verification'
        message = f'Your OTP is: {otp}'
        recipient_list = [user.email]

        try:
            send_mail(subject, message,settings.DEFAULT_FROM_EMAIL,recipient_list)
            if user:
                request.session['user_id'] = user.id
            print(request.session.get('user_id'))
            return Response({'user_id': user.id},status=status.HTTP_200_OK)
        except smtplib.SMTPException as e:
            # Handle SMTPException (e.g., connection issues, authentication failure, etc.)
            print(f"Error sending email: {e}")
            return Response({"error": "Error sending OTP via email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def partial_update(self, request, *args, **kwargs):
        """
        Confirm the OTP
        """
        print(request.data)
        id = self.kwargs.get('pk')
        print(id)

        # user_id = request.session.get('user_id')

        # print(user_id)


        if not id:
            return Response({'message': "Your session is expired"}, status=status.HTTP_401_UNAUTHORIZED)
            print('1')

        if  id:
            user = UserAccount.objects.get(id=id)
            print(user.otp)

            provided_otp = request.data.get('data', {}).get('otp')

            if provided_otp and user.otp == provided_otp:
                user.otp = True
                user.save()
                return Response({'message': "OTP verified successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({'message': "Invalid OTP"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': "User ID mismatch"}, status=status.HTTP_401_UNAUTHORIZED)
    
class ResetPassword(viewsets.ModelViewSet):
    """
    Function for reset the password
    """
    queryset = UserAccount.objects.all()
    serializer_class = UserDetailsSerilzer

    def partial_update(self, request, *args, **kwargs):
        """
        Update the password
        """
        print(request.data)
        data = request.data
        user_id = self.kwargs.get('pk')

        if UserAccount.objects.get(id=user_id).otp == True:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            user = UserAccount.objects.get(id=user_id)
        except UserAccount.DoesNotExist:
            return Response({'Message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if OTP is set
        if user.otp:
            new_password = data.get('data', {}).get('newPassword')
            confirm_password = data.get('data', {}).get('confirmPassword')

            if new_password == confirm_password:
                # Use the reset_password method if implemented in your UserAccount model
                user.set_password(confirm_password)
                user.save()
                return Response({'Message': "Password is changed successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({'Message': "New and confirm passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Message': "OTP not set for the user"}, status=status.HTTP_400_BAD_REQUEST)
            


class Dashboard(viewsets.ModelViewSet):
    """
    Dashboard is for superadmin
    """
    queryset = RegisterCollege.objects.all()
    serializer_class = None

    def list(self, request, *args, **kwargs):
        total_count = RegisterCollege.objects.all().count()
        verified_colleges_count = RegisterCollege.objects.filter(verified=True).count()

        data = {'total_count': total_count, 'verified_colleges_count': verified_colleges_count}
        return Response(data, status=status.HTTP_200_OK)
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    """
    Manager For creating the user and the superuser
    """
    # def create_user(self,first_name,last_name,email,password=None):

    #     if not email:
    #         raise ValueError("Users must have an email address")

    #     email = self.normalize_email(email)
    #     email = email.lower()

    #     user = self.model(
    #         first_name = first_name,
    #         last_name=last_name,
    #         email = email,

    #     )

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)
        
        user = self.model(
            email=email,
            **extra_fields
        )
        

        user.set_password(password)
        user.save(using=self._db)
        return user
    

    # def create_superuser(self, first_name, last_name,email,password=None):
    #     """
    #     Creates and saves a superuser with the given email, date of
    #     birth and password.
    #     """
    #     user = self.create_user(
    #         first_name,
    #         last_name,
    #         email=email,
    #         password=password,
    #     )
    #     user.is_staff = True
    #     user.is_superuser = True
    #     user.save(using=self._db)
        # return user
    
    def create_superuser(self,email,password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            # first_name,
            # last_name,
            email=email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class UserAccount(AbstractBaseUser):
        """
        User Account model is designed by using the AbstarctBaseuser From the scrath
        """
        
        USER_TYPE = ((1, "College_Admin"), (2, "Staff"), (3, "Student"))

        first_name = models.CharField(max_length=100,blank=True,null=True)
        last_name = models.CharField(max_length=100,blank=True,null=True)
        email = models.EmailField(unique=True,max_length=100)
        is_active = models.BooleanField(default=True)
        is_staff = models.BooleanField(default=True )
        is_superuser =models.BooleanField(default=False)
        user_image = models.ImageField(upload_to='profile',blank=True,null=True)
        phone_number = models.CharField(max_length = 20,blank=True,null=True)
        created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
        updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)
        user_type = models.CharField(default=1, choices=USER_TYPE, max_length=1,blank=True,null=True)
        otp = models.CharField(null=True,blank=True)
        objects = UserManager()

        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = []    




        def has_perm(self, perm, obj=None):
            return self.is_staff

        def has_module_perms(self, app_label):
            return self.is_staff

        def __str__(self):
            return self.email   
        
    
class RegisterCollege(models.Model): 
    """
    Class for register the college
    """

    collegename = models.CharField(max_length = 60)
    state = models.CharField(max_length=40)
    email = models.EmailField()
    is_activate = models.BooleanField(default=False)
    created = models.DateField
    verified = models.BooleanField(default=False)
    details_verified = models.BooleanField(default=False,null=True)
    Verfication_email_status = models.BooleanField(default=False,null=True)
    user_details = models.ForeignKey(UserAccount,on_delete=models.CASCADE,null=True,blank=True)
    primary_password = models.CharField(max_length=100,null=True,blank=True)
    subscription = models.BooleanField(null=True)

    def __str__(self):

        return self.collegename



from django.db import models
from django.contrib.auth.base_user import BaseUserManager,AbstractBaseUser

# class UserManager(BaseUserManager):
#     def create_user(self,email,firstname,surname,password,**extra_keyword):
#         if email is None:
#             ValueError("Email is None")
#         if password is None:
#             ValueError("Password is Not Given")
#         if firstname is None:
#             ValueError("First Name is Not Given")
#         if surname is None:
#             ValueError("SurName is Not Given")
#         user = self.model(email=self.normalize_email(email),firstname=firstname,surname=surname)
#         user.set_password(password)
#         user.save()
#         return user

#     def create_superuser(self,email,firstname,surname,password,**extra_keyword):
#         user = self.create_user(email,firstname,surname,password,**extra_keyword)
#         user.is_superuser=True
#         user.is_staff = True
#         user.is_admin = True
#         return user


class CustomManager(BaseUserManager):
    def create_user(self,email=None,firstname=None,surname=None,password=None,**extra_kargs):
        if not email:
            raise ValueError("Email Mangta mereko")
        if not firstname:
            raise ValueError("First Name Mangta mereko")
        if not surname:
            raise ValueError("SurName Mangta mereko")
        if not password:
            raise ValueError("Password bhi mangta")
        user = self.model(email=self.normalize_email(email),firstname = firstname,surname=surname)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email=None,firstname=None,surname=None,password=None,**extra_kargs):
        user = self.create_user(email,firstname,surname,password,**extra_kargs)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser):
    firstname=models.CharField(max_length=64,null=False)
    surname=models.CharField(max_length=64,null=False)
    mobile=models.CharField(max_length=13,null=False)
    email=models.EmailField(max_length=50,primary_key=True,null=False,unique=True)
    password=models.CharField(max_length=100,null=False)
    birth_date=models.DateTimeField(null=True)
    gender=models.CharField(max_length=10)
    image=models.ImageField(upload_to='DatabaseImage',blank=True)
    profile=models.ImageField(upload_to='Profile',blank=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['firstname','surname','mobile']
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = CustomManager()
    def __str__(self):
        return self.firstname +" "+self.surname


    def has_perm(self,perm,obj=None):
        return True
    def has_module_perms(self,app_label):
        return True


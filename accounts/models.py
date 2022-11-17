from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin, UserManager


# class CustomUser(BaseUserManager):
#     def create_user(self, email, username, first_name, last_name, avatar, phone_number, password
#                     ):
#         # if not email:
#         #     raise ValueError('Users must have an email address')
#
#         user = self.model(
#             email=self.normalize_email(email),
#             first_name=first_name,
#             last_name=last_name,
#             avatar=avatar,
#             phone_number=phone_number,
#             username=username
#         )
#
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

    # def create_superuser(self, username, password):
    #     if password is None:
    #         raise TypeError('Password Required')
    #
    #     user = self.create_user(username=username, password=password)
    #     user.is_superuser = True
    #     user.is_staff = True
    #     user.save()
    #
    #     return user


class Users(AbstractUser):
    password = models.CharField(max_length=150, null=True, blank=True)
    # username = models.CharField(max_length=25, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    # classes_lst = models.ManyToManyField(Classes, default=None)
    # class_lst = models.ManyToManyField(Class, default=None)

    email = models.EmailField(verbose_name='Email Address', null=True, blank=True)
    avatar = models.ImageField(upload_to='accounts/images', height_field=None, width_field=None, max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=150, null=True, blank=True)

    is_staff = models.BooleanField(default=False)

    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = []
    #
    # objects = CustomUser()
    # objects = UserManager()

    def __str__(self):
        return self.username
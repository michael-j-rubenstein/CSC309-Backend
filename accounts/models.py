from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser


class CustomUser(BaseUserManager):
    def create_user(self, email=None, username=None, first_name=None, last_name=None, avatar=None, phone_number=None, password=None
                    ):
        # if not email:
        #     raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            avatar=avatar,
            phone_number=phone_number,
            username=username
        )
        print(password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username=username, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class Users(AbstractBaseUser):
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    # classes_lst = models.ManyToManyField(Classes, default=None)
    # class_lst = models.ManyToManyField(Class, default=None)
    password = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(verbose_name='Email Address', null=True, blank=True)
    avatar = models.ImageField(upload_to='accounts/images', height_field=None, width_field=None, max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=150, null=True, blank=True)
    username = models.CharField(max_length=25, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUser()

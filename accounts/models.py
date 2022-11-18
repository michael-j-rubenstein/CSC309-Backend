from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    password = models.CharField(max_length=150, null=True, blank=True)
    password2 = models.CharField(max_length=150, null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(verbose_name='Email Address', null=True, blank=True)
    avatar = models.ImageField(upload_to='accounts/images', height_field=None, width_field=None, max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=150, null=True, blank=True)

    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.username


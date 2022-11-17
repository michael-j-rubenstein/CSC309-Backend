from django.contrib import admin
from django.contrib.admin import register

# from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from accounts.models import Users, CustomUser


# class UserProfileInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False
#
# class AccountsUserAdmin(AuthUserAdmin):
#     def add_view(self, *args, **kwargs):
#         self.inlines =[]
#         return super(AccountsUserAdmin, self).add_view(*args, **kwargs)
#
#     def change_view(self, *args, **kwargs):
#         self.inlines =[UserProfileInline]
#         return super(AccountsUserAdmin, self).change_view(*args, **kwargs)
#
#
# admin.site.unregister(User)
# admin.site.register(User, AccountsUserAdmin)
#
# @register(Users)
# class UserProfile(admin.ModelAdmin):
#     fields = ['email', 'first_name', 'last_name', 'avatar', 'phone_number', 'username', 'password']

# class AccountsUserAdmin(AuthUserAdmin):
#     # fields = ['email', 'first_name', 'last_name', 'avatar', 'phone_number', 'username', 'password']
#     list_display = ['email', 'first_name', 'last_name', 'avatar', 'phone_number', 'username', 'password']
#
#     class Meta:
#         model = CustomUser
#     def __str__(self):
#         return self.username



admin.site.register(Users)

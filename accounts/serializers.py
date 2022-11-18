# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers
from accounts.models import Users
# from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'avatar', 'phone_number')

    # overidding the create user method in the model for my custom user
    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        user = Users.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('email', 'first_name', 'last_name', 'avatar', 'phone_number')

    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError({"password": "Error: Password fields didn't match."})
    #
    #     return attrs
    #
    # def save(self, password=None, **kwargs):
    #     user = Users(username=self.validated_data['username'],
    #                  email=self.validated_data['email'],
    #                  first_name=self.validated_data['first_name'],
    #                  last_name=self.validated_data['last_name'],
    #                  phone_number=self.validated_data['phone_number'],
    #                  avatar=self.validated_data['avatar'])
    #     user.set_password(password)
    #     user.save()

    # class LoginSerializer(serializers.Serializer):
    #     email = serializers.CharField(max_length=255)
    #     username = serializers.CharField(max_length=255, read_only=True)
    #     password = serializers.CharField(max_length=128, write_only=True)
    #     token = serializers.CharField(max_length=255, read_only=True)
    #
    #     def validate(self, data):
    #         # The `validate` method is where we make sure that the current
    #         # instance of `LoginSerializer` has "valid". In the case of logging a
    #         # user in, this means validating that they've provided an email
    #         # and password and that this combination matches one of the users in
    #         # our database.
    #         email = data.get('email', None)
    #         password = data.get('password', None)
    #
    #         # Raise an exception if an
    #         # email is not provided.
    #         if email is None:
    #             raise serializers.ValidationError(
    #                 'An email address is required to log in.'
    #             )
    #
    #         # Raise an exception if a
    #         # password is not provided.
    #         if password is None:
    #             raise serializers.ValidationError(
    #                 'A password is required to log in.'
    #             )
    #
    #         # The `authenticate` method is provided by Django and handles checking
    #         # for a user that matches this email/password combination. Notice how
    #         # we pass `email` as the `username` value since in our User
    #         # model we set `USERNAME_FIELD` as `email`.
    #         user = authenticate(username=email, password=password)
    #
    #         # If no user was found matching this email/password combination then
    #         # `authenticate` will return `None`. Raise an exception in this case.
    #         if user is None:
    #             raise serializers.ValidationError(
    #                 'A user with this email and password was not found.'
    #             )
    #
    #         # Django provides a flag on our `User` model called `is_active`. The
    #         # purpose of this flag is to tell us whether the user has been banned
    #         # or deactivated. This will almost never be the case, but
    #         # it is worth checking. Raise an exception in this case.
    #         if not user.is_active:
    #             raise serializers.ValidationError(
    #                 'This user has been deactivated.'
    #             )
    #
    #         # The `validate` method should return a dictionary of validated data.
    #         # This is the data that is passed to the `create` and `update` methods
    #         # that we will see later on.
    #         return {
    #             'email': user.email,
    #             'username': user.username,
    #             'token': user.token
    #         }
    #
    # def save(self, request):
    #     adapter = get_adapter()
    #     user = adapter.new_user(request)
    #     self.cleaned_data = self.get_cleaned_data()
    #     adapter.save_user(request, user, self)
    #     setup_user_email(request, user, [])
    #
    #     user.address = self.cleaned_data.get('address')
    #     user.user_type = self.cleaned_data.get('user_type')
    #
    #     user.save()
    #     return user

    # def save(self, **kwargs):
    #     print(self)
    # def create(self, validated_data):
    #     user = Users.objects.create_user(**validated_data)
    #     user.save()
    #     return user
    # def create(self, validated_data):
    #     # Use the `create_user` method we wrote earlier to create a new user.
    #     return Users.objects.create_user(**validated_data)

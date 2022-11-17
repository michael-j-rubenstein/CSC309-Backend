# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from accounts.models import Users
# from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('email', 'first_name', 'last_name', 'avatar', 'phone_number', 'username', 'password')

    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError({"password": "Error: Password fields didn't match."})
    #
    #     return attrs
    #
    def get_cleaned_data(self):
        data = super(RegisterSerializer, self).get_cleaned_data()
        print('clean data', data)
        return {
            'username': self.validated_data.get('username', ''),
            'password': self.validated_data.get('password', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
            'avatar': self.validated_data.get('avatar', '')
        }
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
    def create(self, validated_data):
        user = Users.objects.create_user(**validated_data)
        print(validated_data.data)
        user.save()
        return user
    # def create(self, validated_data):
    #     # Use the `create_user` method we wrote earlier to create a new user.
    #     return Users.objects.create_user(**validated_data)


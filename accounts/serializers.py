from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from accounts.models import Users


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('username', 'password', 'email', 'first_name',
                  'last_name', 'avatar', 'phone_number', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"Error: The two password fields didn't match"})

        return attrs

    def create(self, validated_data):
        user = Users.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('email', 'first_name', 'last_name', 'avatar',
                  'phone_number')


class MePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('email', 'first_name', 'last_name', 'avatar', 'phone_number')

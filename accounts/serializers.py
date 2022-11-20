from rest_framework import serializers
from accounts.models import Users


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'avatar', 'phone_number')

    def create(self, validated_data):
        user = Users.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('email', 'first_name', 'last_name', 'avatar', 'phone_number')

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_repeat = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_repeat')
        ordering = ['username']

    def validate(self, attrs):
        password_repeat = attrs.pop('password_repeat', None)
        password = attrs.get('password')

        if password_repeat != password:
            raise ValidationError('Passwords do not match')
        return attrs

    def create(self, validated_data: dict) -> CustomUser:
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password')

    def validate(self, attrs: dict) -> dict:
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError('password or username is not correct')
        attrs["user"] = user
        return attrs


class UserRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UserPasswordUpdateSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = serializers.CharField(min_length=1, required=True, write_only=True)
    new_password = serializers.CharField(min_length=1, required=True, write_only=True, validators=[validate_password])

    def validate(self, attrs: dict) -> dict:
        """
        Переопределил пустой validate для проверки пароля, так же достаю и удаляю password_repeat.
        """
        password_old = attrs.get('old_password')

        user: CustomUser = self.instance
        if not user.check_password(password_old):
            raise ValidationError({'old_password': 'is incorrect'})
        return attrs

    def update(self, instance: CustomUser, validated_data: dict):
        instance.set_password(validated_data['new_password'])
        instance.save(update_fields=['password'])
        return instance

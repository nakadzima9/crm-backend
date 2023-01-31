from rest_framework import serializers
from users.models import User
from .custom_funcs import validate_phone, validate_email, create, validate


class RegisterAdminSerializer(serializers.ModelSerializer):
    user_type = serializers.HiddenField(default='manager')
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'email',
                  'password',
                  'user_type']
        read_only_fields = ['user_type', 'is_superuser']

    def validate(self, data):
        return validate(self, data, User, RegisterAdminSerializer)

    def validated_email(self, value):
        return validate_email(value)

    def validate_phone(self, value):
        return validate_phone(value)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save()
        return user


class RegisterStudentSerializer(serializers.ModelSerializer):
    user_type = serializers.HiddenField(default='traveler')
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'password',
            'email',
            'user_type',
        ]

    def validate(self, data):
        return validate(self, data, User, RegisterTravelerSerializer)

    def validate_email(self, value):
        return validate_email(value)

    def validate_phone(self, value):
        return validate_phone(value)

    def create(self, validated_data):
        return create(validated_data, User)



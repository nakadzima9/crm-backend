from rest_framework import serializers, response
import django.contrib.auth.password_validation as validators

from cmsapp.api.serializers import DepartmentSerializer, GroupSerializer, ScheduleTypeSerializer
from users.models import User, OTP, Mentor
from .custom_funcs import validate_phone, validate_email, create, validate


class UserSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'email',
                  'phone',
                  'user_type',
                  'image',
                  # 'description',
                  # 'sex',
                  ]

    read_only_fields = ['user_type']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            image_url = obj.image.url
            return request.build_absolute_uri(image_url)
        else:
            return None


class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'email',
                  'password',
                  'phone',
                  'image',
                  # 'description',
                  # 'sex',
                  ]


    def validate(self, data):
        return validate(self, data, User, AdminSerializer)

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
        user.user_type = 'admin'
        user.save()
        return user


class ManagerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'email',
                  'password',
                  'phone',
                  'image',
                  # 'description',
                  # 'sex',
                  ]


    def validate(self, data):
        return validate(self, data, User, ManagerSerializer)

    def validate_email(self, value):
        return validate_email(value)

    def validate_phone(self, value):
        return validate_phone(value)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.is_staff = True
        user.set_password(password)
        user.user_type = 'manager'
        user.save()
        return user


class MentorSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    group = GroupSerializer(read_only=True)
    schedule_type = ScheduleTypeSerializer(read_only=True)

    class Meta:
        model = Mentor
        fields = ['id',
                  'first_name',
                  'last_name',
                  'email',
                  'phone',
                  'image',
                  'group',
                  'department',
                  'schedule_type',
                  'patent_number',
                  'patent_start',
                  'patent_end',
                  # 'description',
                  # 'sex',
                  ]


    def validate_email(self, value):
        return validate_email(value)

    def validate_phone(self, value):
        return validate_phone(value)

    def create(self, validated_data):
        mentor = Mentor(**validated_data)
        mentor.user_type = 'mentor'
        mentor.save()
        return mentor


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'email',
                  'phone',
                  'image',
                  # 'description',
                  # 'sex',
                  ]

    def validate_phone(self, value):
        return validate_phone(value)


class UserSerializerWithoutEmail(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'phone',
                  'image',
                  # 'description',
                  # 'sex',
                  ]


    def validate_phone(self, value):
        return validate_phone(value)


class AdminSerializerWithoutEmail(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'phone',
                  'image',
                  # 'description',
                  # 'sex',
                  ]


    def validate_phone(self, value):
        return validate_phone(value)


class ManagerSerializerWithoutEmail(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'phone',
                  'image',
                  # 'description',
                  # 'sex',
                  ]


    def validate_phone(self, value):
        return validate_phone(value)


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    repeat_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('password', 'repeat_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['repeat_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def update(self, instance, validated_data):
        validators.validate_password(user=instance, password=validated_data['password'])
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class PasswordCheckEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]


class PasswordCodeCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ["code"]

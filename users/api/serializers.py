from rest_framework import serializers, response
from jwt import decode as jwt_decode
from rest_framework_simplejwt.serializers import TokenVerifySerializer as _TokenVerifySerializer
from rest_framework_simplejwt.tokens import UntypedToken, RefreshToken
from rest_framework.exceptions import ValidationError

from core import settings
from users.models import User, OTP
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
                  # 'image',
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
                  # 'image',
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
                  # 'image',
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
    class Meta:
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'email',
                  'phone',
                  # 'image',
                  # 'description',
                  # 'sex',
                  ]


    def validate_email(self, value):
        return validate_email(value)

    def validate_phone(self, value):
        return validate_phone(value)

    def create(self, validated_data):
        user = User(**validated_data)
        user.user_type = 'teacher'
        user.save()
        return user


class TokenVerifySerializer(_TokenVerifySerializer):

    def validate(self, attrs):
        UntypedToken(attrs['token'])
        data = jwt_decode(attrs['token'], settings.SECRET_KEY, algorithms=['HS256'])
        user_data = User.objects.get(id=data['user_id'])
        refresh = RefreshToken.for_user(user_data)
        data = {
            'access_token': str(refresh.access_token),
            'id': data['user_id'],
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'email': user_data.email,
            'phone': user_data.phone,
            'user_type': user_data.user_type,
        }

        return data


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

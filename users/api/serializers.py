from rest_framework import serializers, response
from jwt import decode as jwt_decode
from rest_framework_simplejwt.serializers import TokenVerifySerializer as _TokenVerifySerializer
from rest_framework_simplejwt.tokens import UntypedToken, RefreshToken
from rest_framework.exceptions import ValidationError

from core import settings
from users.models import User, OTP


class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image_url')

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
                  'user_type',
                  ]

    read_only_fields = ['user_type']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            image_url = obj.image.url
            return request.build_absolute_uri(image_url)
        else:
            return None


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
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
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
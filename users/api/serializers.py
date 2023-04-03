# from cloudinary_storage.storage import MediaCloudinaryStorage
from rest_framework import serializers
import django.contrib.auth.password_validation as validators

from cmsapp.api.serializers import DepartmentSerializer, GroupSerializer
from core import settings
from users.models import User, OTP
from .custom_funcs import validate_phone, validate_email, password_reset_validate

import boto3


class UserSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField('get_image_url')
    fio = serializers.SerializerMethodField('get_fio')

    class Meta:
        model = User
        fields = [
            'id',
            'fio',
            'first_name',
            'last_name',
            'email',
            'phone',
            'user_type',
            'image',
            'is_active'
        ]

    read_only_fields = ['user_type']

    def get_fio(self, obj):
        return obj.first_name + ' ' + obj.last_name

    # def get_image_url(self, obj):
    #     request = self.context.get('request')
    #     if obj.image and hasattr(obj.image, 'url'):
    #         image_url = obj.image.url
    #         return request.build_absolute_uri(image_url)
    #     else:
    #         return None


class UserArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'is_active',
        ]


class AdminSerializer(serializers.ModelSerializer):
    fio = serializers.SerializerMethodField('get_fio')

    class Meta:
        model = User
        fields = [
            'id',
            'fio',
            'first_name',
            'last_name',
            'email',
            'phone',
            'image',
            'is_active',
        ]

    def get_fio(self, obj):
        return obj.first_name + ' ' + obj.last_name

    def validated_email(self, value):
        return validate_email(value)

    def validate_phone(self, value):
        return validate_phone(self, value)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_superuser = True
        user.is_staff = True
        user.user_type = 'admin'
        user.save()
        return user


class ManagerSerializer(serializers.ModelSerializer):
    fio = serializers.SerializerMethodField('get_fio')

    class Meta:
        model = User
        fields = [
            'id',
            'fio',
            'first_name',
            'last_name',
            'email',
            'phone',
            'image',
            'is_active',
        ]

    def get_fio(self, obj):
        return obj.first_name + ' ' + obj.last_name

    def validate_email(self, value):
        return validate_email(value)

    def validate_phone(self, value):
        return validate_phone(self, value)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_staff = True
        user.user_type = 'manager'
        user.save()
        return user


class MentorListSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'image',
            'department',
            'linkedin',
        ]


class MentorDetailSerializer(serializers.ModelSerializer):
    # department = DepartmentSerializer(read_only=True)
    # group_set = GroupSerializer(read_only=True, many=True)
    group_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'image',
            'linkedin',
            'group_set',
            'department',
            'patent_number',
            'patent_start',
            'patent_end',
            'is_active',
        ]

    def validate_email(self, value):
        return validate_email(value)

    def validate_phone(self, value):
        return validate_phone(self, value)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data, without_generate_password=True)
        user.user_type = 'mentor'
        user.save()
        return user


class MentorArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'is_active',
        ]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'image',
        ]

    def validate_phone(self, value):
        return validate_phone(self, value)


class ProfileSerializerOnlyWithImage(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'image',
        ]

    # def update(self, instance, validated_data):
    #     storage = MediaCloudinaryStorage()
    #     storage.delete(name=instance.image.name)
    #     instance.image = validated_data.get('image', instance.image)
    #     instance.save()
    #     return instance

    def update(self, instance, validated_data):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        image = validated_data.get('image', instance.image)
        instance.image = image
        instance.save()
        try:
            s3_client.get_object(
                Bucket='cms-neolabs',
                Key=instance.image.name,
            )
            return instance
        except s3_client.exceptions.NoSuchKey:
            raise serializers.ValidationError("The image was not uploaded")


class UserSerializerWithoutEmailAndImage(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, read_only=True)
    image = serializers.ImageField(required=False, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'image',
        ]

    def validate_phone(self, value):
        return validate_phone(self, value)


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    repeat_password = serializers.CharField(write_only=True, required=True)
    unique_id = serializers.SlugField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'password',
            'repeat_password',
            'unique_id'
        )

    def validate(self, data):
        return password_reset_validate(self, data, ChangePasswordSerializer)

    def update(self, instance, validated_data):
        validators.validate_password(user=instance, password=validated_data['password'])
        instance.set_password(validated_data['password'])
        # instance.save(update=True)
        instance.save()
        return instance


class PasswordEmailCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email"
        ]


class PasswordCodeCheckSerializer(serializers.ModelSerializer):
    unique_id = serializers.SlugField(write_only=True, required=True)
    code = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = OTP
        fields = [
            "code",
            "unique_id"
        ]

# from cloudinary_storage.storage import MediaCloudinaryStorage
from rest_framework import serializers
import django.contrib.auth.password_validation as validators

from cmsapp.api.serializers import DepartmentNameSerializer, GroupNameSerializer
from cmsapp.models import DepartmentOfCourse
from core import settings
from users.models import User, OTP
from patches.custom_funcs import validate_phone, validate_email, password_reset_validate

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
        return f"{obj.first_name} {obj.last_name}"

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
        return f"{obj.first_name} {obj.last_name}"

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
        return f"{obj.first_name} {obj.last_name}"

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
    department = DepartmentNameSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'image',
            'department',
            'linkedin',
            'email',
            'phone',
        ]


def object_not_found_validate(obj: object, name: object) -> object:

    if name is None:
        raise serializers.ValidationError('Departament name does note exist')

    data = obj.filter(name=name).first()

    if not data:
        raise serializers.ValidationError(f"Object {name} does not exist.")
    return data


class MentorDetailSerializer(serializers.ModelSerializer):
    department = DepartmentNameSerializer()
    group_set = GroupNameSerializer(read_only=True, many=True)

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
        department_data = validated_data.pop('department')['name']
        dep = object_not_found_validate(DepartmentOfCourse.objects, department_data)

        user = User.objects.create_user(department=dep, **validated_data, without_generate_password=True)
        user.user_type = 'mentor'
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.image = validated_data.get('image', instance.image)
        instance.linkedin = validated_data.get('linkedin', instance.linkedin)
        instance.patent_number = validated_data.get('patent_number', instance.patent_number)
        instance.patent_start = validated_data.get('patent_start', instance.patent_start)
        instance.patent_end = validated_data.get('patent_end', instance.patent_end)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        department = validated_data.get('department', instance.department)

        if isinstance(department, DepartmentOfCourse):
            department_name = department.name
        else:
            department_name = department.get('name', None)

        instance.department = object_not_found_validate(DepartmentOfCourse.objects, department_name)
        instance.save()
        return instance


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
    image = serializers.ImageField(required=True)

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

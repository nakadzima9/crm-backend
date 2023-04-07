from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from cmsapp.models import (
    DepartmentOfCourse,
    GroupStatus,
    Classroom,
    ScheduleType,
    Group,
    AdvertisingSource,
    RequestStatus,
    PaymentMethod,
    Student,
    Payment,
    Reason,
)
from django.utils import timezone
from patches.custom_funcs import validate_phone
# from cloudinary_storage.storage import MediaCloudinaryStorage


class AdvertisingSourceSerializer(ModelSerializer):
    class Meta:
        model = AdvertisingSource
        fields = [
            'id',
            'name'
        ]


class ClassroomSerializer(ModelSerializer):
    class Meta:
        model = Classroom
        fields = [
            'id',
            'name'
        ]


class DepartmentSerializer(ModelSerializer):
    # mentor = serializers.PrimaryKeyRelatedField(
    #     required=False, many=True, queryset=User.objects.filter(user_type='mentor')
    # )

    class Meta:
        model = DepartmentOfCourse
        fields = [
            'id',
            'name',
            'image',
            'duration_month',
            'description',
            'is_archive',
        ]


class ArchiveDepartmentSerializer(ModelSerializer):
    class Meta:
        model = DepartmentOfCourse
        fields = [
            'id',
            'is_archive',
        ]


class DepartmentSerializerOnlyWithImage(serializers.ModelSerializer):

    class Meta:
        model = DepartmentOfCourse
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


class GroupStatusSerializer(ModelSerializer):
    class Meta:
        model = GroupStatus
        fields = [
            'id',
            'status_name'
        ]


class ScheduleTypeSerializer(ModelSerializer):
    class Meta:
        model = ScheduleType
        fields = [
            'id',
            'type_name',
            'start_time',
            'end_time'
        ]


class DepartmentNameSerializer(ModelSerializer):
    class Meta:
        model = DepartmentOfCourse
        fields = ['name']


class GroupNameSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class GroupSerializer(ModelSerializer):
    status = GroupStatusSerializer()
    classroom = ClassroomSerializer()
    department = DepartmentNameSerializer()
    start_at_date = serializers.DateTimeField(format="%d/%m/%Y", input_formats=["%d/%m/%Y", "iso-8601"], default=timezone.now)
    end_at_date = serializers.DateTimeField(format="%d/%m/%Y", input_formats=["%d/%m/%Y", "iso-8601"], default=timezone.now)
    start_at_time = serializers.DateTimeField(format="%H:%M", input_formats=["%H:%M", "iso-8601"], default=timezone.now)
    end_at_time = serializers.DateTimeField(format="%H:%M", input_formats=["%H:%M", "iso-8601"], default=timezone.now)

    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'mentor',
            'department',
            'students_max',
            'status',
            'schedule_type',
            'classroom',
            'is_archive',
            'start_at_date',
            'end_at_date',
            'start_at_time',
            'end_at_time',
        ]

    def create(self, validated_data):
        classroom_data = validated_data.pop("classroom")["name"]
        department_data = validated_data.pop("department")["name"]
        status_data = validated_data.pop("status")["status_name"]

        dep = get_object_or_404(DepartmentOfCourse.objects.all(), name=department_data)
        room = get_object_or_404(Classroom.objects.all(), name=classroom_data)
        sta = get_object_or_404(GroupStatus.objects.all(), status_name=status_data)

        group = Group.objects.create(department=dep, classroom=room, status=sta, **validated_data)
        return group

    def update(self, instance, validated_data):
        classroom_data = validated_data.pop("classroom")["name"]
        department_data = validated_data.pop("department")["name"]
        status_data = validated_data.pop("status")["status_name"]

        dep = get_object_or_404(DepartmentOfCourse.objects.all(), name=department_data)
        room = get_object_or_404(Classroom.objects.all(), name=classroom_data)
        sta = get_object_or_404(GroupStatus.objects.all(), status_name=status_data)

        instance = Group.objects.get(name=instance.name).update(commit=True, department=dep, classroom=room, status=sta, **validated_data)
        return instance


class ArchiveGroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'id',
            'is_archive',
        ]


class RequestStatusSerializer(ModelSerializer):
    class Meta:
        model = RequestStatus
        fields = [
            'id',
            'name'
        ]


class PaymentMethodSerializer(ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = [
            'id',
            'name'
        ]


class ReasonSerializer(ModelSerializer):
    class Meta:
        model = Reason
        fields = [
            'id',
            'name'
        ]


class StudentSerializer(ModelSerializer):
    department = DepartmentNameSerializer()
    payment_method = PaymentMethodSerializer()
    reason = ReasonSerializer(required=False)
    came_from = AdvertisingSourceSerializer()
    status = RequestStatusSerializer(required=False)
    request_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "last_name",
            "surname",
            "notes",
            "phone",
            "laptop",
            "department",
            "came_from",
            "payment_method",
            "status",
            "paid",
            "reason",
            "on_request",
            "request_date",
            "is_archive",
        ]

    def validate_phone(self, value):
        return validate_phone(self, value)

    def create(self, validated_data):
        department_data = validated_data.pop("department")["name"]
        payment_method_data = validated_data.pop("payment_method")["name"]
        came_from_data = validated_data.pop("came_from")["name"]

        dep = self.object_not_found_validate(DepartmentOfCourse.objects, department_data)
        pay = self.object_not_found_validate(PaymentMethod.objects, payment_method_data)
        source = self.object_not_found_validate(AdvertisingSource.objects, came_from_data)

        student = Student(payment_method=pay, department=dep, came_from=source, **validated_data)
        student.save()
        return student

    def update(self, instance, validated_data):
        dep = get_object_or_404(DepartmentOfCourse.objects.all(), name=validated_data.pop("department")["name"])
        source = get_object_or_404(AdvertisingSource.objects.all(), name=validated_data.pop("came_from")["name"])
        payment_method = get_object_or_404(PaymentMethod.objects.all(), name=validated_data.pop("payment_method")["name"])
        status = self.object_not_found_validate(RequestStatus.objects.all(), name=validated_data.pop("status")["name"])

        instance = Student.objects.get(phone=instance.phone, on_request=True).update\
            (
                commit=True,
                department=dep,
                came_from=source,
                payment_method=payment_method,
                status=status,
                **validated_data
            )

        return instance

    def object_not_found_validate(self, obj, name):
        data = obj.get(name=name)

        if not data:
            raise serializers.ValidationError(f"Object {name} does not exist.")
        return data


class StudentOnStudySerializer(ModelSerializer):
    department = DepartmentNameSerializer()
    came_from = AdvertisingSourceSerializer()

    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "last_name",
            "surname",
            "phone",
            "came_from",
            "department",
            'on_request',
            "is_archive",
            "laptop",
            "payment_status",
            'notes',
        ]

    def validate_phone(self, value):
        return validate_phone(self, value)

    def create(self, validated_data):
        department_data = validated_data.pop("department")["name"]
        came_from_data = validated_data.pop("came_from")["name"]

        dep = get_object_or_404(DepartmentOfCourse.objects.all(), name=department_data)
        source = get_object_or_404(AdvertisingSource.objects.all(), name=came_from_data)

        student = Student.objects.create(department=dep, came_from=source, **validated_data)
        return student

    def update(self, instance, validated_data):
        department_data = validated_data.pop("department")["name"]
        came_from_data = validated_data.pop("came_from")["name"]

        dep = get_object_or_404(DepartmentOfCourse.objects.all(), name=department_data)
        source = get_object_or_404(AdvertisingSource.objects.all(), name=came_from_data)

        instance = Student.objects.get(phone=instance.phone, on_request=False).update(commit=True, department=dep, came_from=source, **validated_data)
        return instance


class ArchiveStudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'is_archive',
        ]


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'payment_type',
            'created_at',
            'user',
            'client_card',
            'amount',
        ]

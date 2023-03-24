from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from cmsapp.models import (
    Department,
        GroupStatus,
    Classroom,
    Course,
    ScheduleType,
    Group,
    AdvertisingSource,
    RequestStatus,
    PaymentMethod,
    Student,
    Payment,
    Reason,
)
from users.models import User
from .custom_funcs import validate_phone
from cloudinary_storage.storage import MediaCloudinaryStorage


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


class CourseSerializer(ModelSerializer):
    # mentors = serializers.PrimaryKeyRelatedField(
    #     required=False, many=True, queryset=User.objects.filter(user_type='mentor')
    # )

    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'department',
            # 'mentors',
            'image',
            'duration_month',
        ]


class ArchiveCourseSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'is_archive',
        ]


class CourseSerializerOnlyWithImage(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = [
            'id',
            'image',
        ]

    def update(self, instance, validated_data):
        storage = MediaCloudinaryStorage()
        storage.delete(name=instance.image.name)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = [
            'id',
            'name'
        ]


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


class GroupSerializer(ModelSerializer):
    status = GroupStatusSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    schedule_type = ScheduleTypeSerializer(read_only=True)
    classroom = ClassroomSerializer(read_only=True)

    class Meta:
        model = Group
        fields = [
            'id',
            'number',
            'students_max',
            'status',
            'created_at',
            'course',
            'schedule_type',
            'classroom',
            'is_archive'
        ]


class ArchiveGroupSerializer(ModelSerializer):
    class Meta:
        model = Student
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
    department = DepartmentSerializer()
    payment_method = PaymentMethodSerializer()
    reason = ReasonSerializer(required=False)
    came_from = AdvertisingSourceSerializer()
    status = RequestStatusSerializer(required=False)

    class Meta:
        model = Student
        depth = 1
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
            "is_archive"
        ]

    def validate_phone(self, value):
        return validate_phone(self, value)

    def create(self, validated_data):
        department_data = validated_data.pop("department")["name"]
        payment_method_data = validated_data.pop("payment_method")["name"]
        came_from_data = validated_data.pop("came_from")["name"]

        try:
            dep = Department.objects.get(name=department_data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(f"Object {department_data} does not exist.")
        try:
            pay = PaymentMethod.objects.get(name=payment_method_data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(f"Object {payment_method_data} does not exist.")
        try:
            source = AdvertisingSource.objects.get(name=came_from_data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(f"Object {came_from_data} does not exist.")
        student = Student(department=dep, payment_method=pay, came_from=source, **validated_data)
        student.save()
        return student

    def object_not_found_validate(self, obj, name):
        try:
            data = obj.objects.get(name=name)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(f"Object {name} does not exist.")
        return data

    # def update(self, instance, validated_data):
    #     instance.save()
    #     return instance

    # def get_reason(self, obj):
    #     print(obj)
    #     return Student.objects.filter(reason=1).count()
    #     # stud = Student.objects.all()
    #     # i = stud.objects.filter(reason=1).count

    def update(self, instance, validated_data):
        print(validated_data.get("department")["name"])
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.surname = validated_data.get("surname", instance.surname)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.laptop = validated_data.get("laptop", instance.laptop)
        dep = Department.objects.get(name=validated_data.get("department")["name"])
        instance.department = dep
        source = AdvertisingSource.objects.get(name=validated_data.get("came_from")["name"])
        instance.came_from = source
        method = PaymentMethod.objects.get(name=validated_data.get("payment_method")["name"])
        instance.payment_method = method
        statuss = RequestStatus.objects.get(name=validated_data.get("status")["name"])
        instance.status = statuss
        instance.paid = validated_data.get("paid", instance.paid)
        # reason = Reason.objects.get(name=validated_data.get("reason")["name"])
        # instance.reason = reason
        instance.save()
        return instance


class StudentOnStudySerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "last_name",
            "surname",
            "phone",
            "department",
            "payment_method",
        ]


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

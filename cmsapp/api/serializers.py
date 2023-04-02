from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from cmsapp.models import (
    Department,
    GroupStatus,
    Classroom,
    # Course,
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
        model = Department
        fields = [
            'id',
            'name',
            'image',
            'duration_month',
            'description',
            'is_archive',
        ]


# class ArchiveCourseSerializer(ModelSerializer):
#     class Meta:
#         model = Course
#         fields = [
#             'id',
#             'is_archive',
#         ]


class DepartmentSerializerOnlyWithImage(serializers.ModelSerializer):

    class Meta:
        model = Department
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


# class DepartmentSerializer(ModelSerializer):
#     class Meta:
#         model = Department
#         fields = [
#             'id',
#             'name'
#         ]


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
    course = DepartmentSerializer(read_only=True)
    schedule_type = ScheduleTypeSerializer(read_only=True)
    classroom = ClassroomSerializer(read_only=True)

    class Meta:
        model = Group
        fields = [
            'id',
            'number',
            'mentor',
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


class DepartmentNameSrializer(ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']


class StudentSerializer(ModelSerializer):
    department = DepartmentNameSrializer()
    payment_method = PaymentMethodSerializer()
    reason = ReasonSerializer(required=False)
    came_from = AdvertisingSourceSerializer()
    status = RequestStatusSerializer(required=False)
    request_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    # request_time = serializers.TimeField(format="%H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Student
        # depth = 1
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
            # "request_time",
            "is_archive",
        ]

    def validate_phone(self, value):
        return validate_phone(self, value)

    def create(self, validated_data):
        department_data = validated_data.pop("department")["name"]
        payment_method_data = validated_data.pop("payment_method")["name"]
        came_from_data = validated_data.pop("came_from")["name"]

        dep = self.object_not_found_validate(Department.objects, department_data)
        pay = self.object_not_found_validate(PaymentMethod.objects, payment_method_data)
        source = self.object_not_found_validate(AdvertisingSource.objects, came_from_data)

        student = Student(payment_method=pay, department=dep, came_from=source, **validated_data)
        student.save()
        return student

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.surname = validated_data.get("surname", instance.surname)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.laptop = validated_data.get("laptop", instance.laptop)
        instance.on_request = validated_data.get("on_request", instance.on_request)
        instance.paid = validated_data.get("paid", instance.paid)
        instance.department = validated_data.get("department", instance.department)

        instance.department = self.object_not_found_validate(Department.objects,
                                                             validated_data.get("department")["name"])
        instance.came_from = self.object_not_found_validate(AdvertisingSource.objects,
                                                            validated_data.get("came_from")["name"])
        instance.payment_method = self.object_not_found_validate(PaymentMethod.objects,
                                                                 validated_data.get("payment_method")["name"])
        instance.status = self.object_not_found_validate(RequestStatus.objects,
                                                         validated_data.get("status")["name"])
        instance.save()
        return instance

    def object_not_found_validate(self, obj, name):
        data = obj.get(name=name)

        if not data:
            raise serializers.ValidationError(f"Object {name} does not exist.")
        return data


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
            'learning_status',
            'on_request',
            "is_archive",
            "laptop",
            "payment_status",
            'notes',
        ]

    def validate_phone(self, value):
        return validate_phone(self, value)


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

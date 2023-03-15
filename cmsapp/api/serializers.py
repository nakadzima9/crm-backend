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
    # AdvertisingSource,
    # RequestStatus,
    PaymentMethod,
    Student,
    Payment,
)
from .custom_funcs import validate_phone


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class GroupStatusSerializer(ModelSerializer):
    class Meta:
        model = GroupStatus
        fields = "__all__"


class ClassroomSerializer(ModelSerializer):
    class Meta:
        model = Classroom
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class ScheduleTypeSerializer(ModelSerializer):
    class Meta:
        model = ScheduleType
        fields = "__all__"


class GroupSerializer(ModelSerializer):
    status = GroupStatusSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    schedule_type = ScheduleTypeSerializer(read_only=True)
    classroom = ClassroomSerializer(read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'number', 'students_max', 'status', 'created_at', 'course', 'schedule_type', 'classroom']


# class AdvertisingSourceSerializer(ModelSerializer):
#     class Meta:
#         model = AdvertisingSource
#         fields = "__all__"
#
#
# class RequestStatusSerializer(ModelSerializer):
#     class Meta:
#         model = RequestStatus
#         fields = "__all__"


class PaymentMethodSerializer(ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = "__all__"


class StudentSerializer(ModelSerializer):
    department = DepartmentSerializer()
    payment_method = PaymentMethodSerializer()
    # reason = serializers.SerializerMethodField()

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
        ]

    def validate_phone(self, value):
        return validate_phone(value)

    def create(self, validated_data):
        department_data = validated_data.pop("department")["name"]
        payment_method_data = validated_data.pop("payment_method")["name"]
        # dep = self.object_not_found_validate(Department, department_data)
        # pay = self.object_not_found_validate(PaymentMethod, payment_method_data)
        try:
            dep = Department.objects.get(name=department_data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(f"Object {department_data} does not exist.")
        try:
            pay = PaymentMethod.objects.get(name=payment_method_data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(f"Object {payment_method_data} does not exist.")
        student = Student(department=dep, payment_method=pay, **validated_data)
        student.save()
        return student

    def object_not_found_validate(self, obj, name):
        try:
            data = obj.objects.get(name=name)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(f"Object {name} does not exist.")
        return data

    # def get_reason(self, obj):
    #     print(obj)
    #     return Student.objects.filter(reason=1).count()
    #     # stud = Student.objects.all()
    #     # i = stud.objects.filter(reason=1).count

    # def update(self, instance, validated_data):
    #     instance.first_name = validated_data.pop("first_name")
    #     instance.last_name = validated_data.pop("last_name")
    #     instance.surname = validated_data.pop("surname")
    #     instance.notes = validated_data.pop("notes")
    #     instance.phone = validated_data.pop("phone")
    #     instance.laptop = validated_data.pop("laptop")
    #     instance.department = validated_data.pop("department")
    #     instance.came_from = validated_data.pop("came_from")
    #     instance.payment_method = validated_data.pop("payment_method")
    #     instance.status = validated_data.pop("status")
    #     instance.paid = validated_data.pop("paid")
    #     instance.reason = validated_data.pop("reason")
    #     instance.save()
    #     return instance


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


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
